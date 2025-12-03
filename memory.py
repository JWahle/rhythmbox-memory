import gi
gi.require_version('RB', '3.0')
gi.require_version('Peas', '1.0')
from gi.repository import GObject, RB, Peas
import json
import os

class MemoryPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'MemoryPlugin'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(MemoryPlugin, self).__init__()
        self.state_file = os.path.expanduser('~/.local/share/rhythmbox/plugins/memory/state.json')

    def do_activate(self):
        print("Memory Plugin activating")
        self.shell = self.object
        self.player = self.shell.props.shell_player
        self.handler_id = self.player.connect('playing-song-changed', self._save_current_track)
        GObject.timeout_add(2000, self._restore_last_track)

    def do_deactivate(self):
        print("Memory Plugin deactivating")
        self.player.disconnect(self.handler_id)
        self.shell = None
        self.player = None

    def _save_current_track(self, player, entry):
        source = player.get_playing_source()
        if entry and source:
            uri = entry.get_string(RB.RhythmDBPropType.LOCATION)
            source_name = source.props.name
            state = {'uri': uri, 'source': source_name}
            try:
                os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
                with open(self.state_file, 'w') as f:
                    json.dump(state, f)
                print(f"Saved state: {state}")
            except Exception as e:
                print(f"Error saving state: {e}")

    def _restore_last_track(self):
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            print(f"Trying to restore state: {state}")
            uri = state.get('uri')
            source_name = state.get('source')
            if uri:
                db = self.shell.props.db
                entry = db.entry_lookup_by_location(uri)
                if entry:
                    source = self._source_with_name(source_name)
                    self.player.play_entry(entry, source)
                    GObject.timeout_add(200, self._pause_player)
                    print(f"Restored state: {uri} from {source_name or 'library'}")
                else:
                    print(f"Entry not found for URI: {uri}")
        except Exception as e:
            print(f"Error restoring state: {e}")
        return False

    def _pause_player(self):
        self.player.pause()
        return False

    def _source_with_name(self, source_name):
        playlists = self.shell.props.playlist_manager.get_playlists()
        for playlist in playlists:
            if playlist.props.name == source_name:
                return playlist

        builtin_sources = []
        if hasattr(self.shell.props, 'library_source'):
            builtin_sources.append(self.shell.props.library_source)
        if hasattr(self.shell.props, 'podcast_source'):
            builtin_sources.append(self.shell.props.podcast_source)
        for builtin_source in builtin_sources:
            if builtin_source.props.name == source_name:
                return builtin_source

        print(f"Using library source as fallback")
        return self.shell.props.library_source
