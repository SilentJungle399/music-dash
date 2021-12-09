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
			guild: null,
			channel: null,
		},
	},
	mutations: {
		setUser(state, user) {
			state.user = user;
		},
		setSid(state, sid) {
			state.sid = sid;
		},
		switchTab(state) {
			state.tab = "queue" === state.tab ? "search" : "queue";
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
		setShuffle(state, shuffle) {
			state.player.controls.shuffle = shuffle;
		},
		setRepeat(state, repeat) {
			state.player.controls.repeat = repeat;
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
