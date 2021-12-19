import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
	state: {
		user: {},
		sid: "",
		tab: "queue",
		progress: 0,
		queue: [],
		player: {
			paused: false,
			controls: {
				volume: 50,
				shuffle: false,
				repeat: false,
			},
			track: null,
		},
		voice: {
			guild: {
				id: null,
				name: null,
				icon: null,
			},
			channel: {
				id: null,
				name: null,
			},
		},
	},
	mutations: {
		setUser(state, user) {
			state.user = user;
		},
		setInit(state, data) {
			state.player = {
				paused: data.state.paused,
				controls: {
					volume: data.state.volume,
					shuffle: data.state.shuffle,
					repeat: data.state.repeat,
				},
				track: data.current,
			};
			state.queue = data.queue;
			state.progress = data.state.progress;
			state.sid = data.sid;
			state.voice = data.voice;
		},
		setSid(state, sid) {
			state.sid = sid;
		},
		switchTab(state, tab) {
			state.tab = tab;
		},
		setProgress(state, progress) {
			state.progress = progress;
		},
		setQueue(state, queue) {
			state.queue = queue;
		},
		setVolume(state, volume) {
			state.player.controls.volume = volume;
		},
		togShuffle(state) {
			state.player.controls.shuffle = !state.player.controls.shuffle;
		},
		togRepeat(state) {
			state.player.controls.repeat = !state.player.controls.repeat;
		},
		setTrack(state, track) {
			state.player.track = track;
		},
		setPaused(state, paused) {
			state.player.paused = paused;
		},
		setVoice(state, data) {
			state.voice = data;
		},
	},
	actions: {},
	modules: {},
});
