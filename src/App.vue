<template>
	<div id="app">
		<div class="supported" v-if="!unsupported">
			<!-- Application here -->
			<Notification @makealert="makealert" :msg="notif"></Notification>
			<div class="leftsidebar">
				<UserInfo @makealert="makealert"></UserInfo>
				<hr class="sidepanedivider" />
				<SidePane @makealert="makealert"></SidePane>
			</div>

			<div class="apparea">
				<MainArea ref="mainarea" @makealert="makealert"></MainArea>
			</div>
			<PlayerSection @makealert="makealert" :preTrack="track"></PlayerSection>
		</div>
		<div v-else class="unsupported">
			<h3>Unfortunately, your device is not supported for the webapp.</h3>
		</div>
	</div>
</template>

<script>
import Notification from "@/components/utils/Notification.vue";
import progress from "@/handlers/progress.js";
import UserInfo from "@/components/BaseComp/SideBar/UserInfo.vue";
import SidePane from "@/components/BaseComp/SideBar/SidePane.vue";
import MainArea from "@/components/BaseComp/AppArea/MainArea.vue";
import PlayerSection from "@/components/BaseComp/PlayerSection.vue";

export default {
	name: "App",
	components: {
		Notification,
		UserInfo,
		SidePane,
		MainArea,
		PlayerSection,
	},
	data() {
		return {
			notif: null,
			curnotif: null,
			unsupported: false,
			loggedin: false,
			auexists: false,
			track: null,
		};
	},
	methods: {
		makealert(msg) {
			if (this.curnotif) {
				clearTimeout(this.curnotif);
				this.curnotif = null;
			}
			this.notif = msg;
			document.getElementById("notif").style.zIndex = 1000;
			document.getElementById("notif").style.opacity = 1;
			this.curnotif = setTimeout(function () {
				document.getElementById("notif").style.opacity = 0;
				document.getElementById("notif").style.zIndex = 0;
			}, 2500);
		},
		checksize() {
			if (window.innerWidth > 1000) {
				if (this.unsupported) {
					progress.done();
				}
				this.unsupported = false;
			} else {
				progress.start("load");
				this.unsupported = true;
			}
		},
		random(length, randomString = "") {
			randomString += Math.random().toString(36).substr(2, length);
			if (randomString.length > length) return randomString.slice(0, length);
			return this.random(length, randomString);
		},
	},
	mounted() {
		const token = this.$cookies.get("token");
		if (!token) {
			window.location.href =
				"https://discord.com/api/oauth2/authorize?client_id=740568766198448190&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback&response_type=code&scope=identify";
			return;
		}
		progress.start("page");

		this.$store.commit("switchTab", "queue");

		if (window.innerWidth > 1000) {
			this.unsupported = false;
		} else {
			this.unsupported = true;
		}
	},
	sockets: {
		error(data) {
			if (data.redirect) {
				window.location.href = data.redirect;
			} else {
				this.makealert(data.message);
			}
		},
		userResponse(data) {
			this.$store.commit("setUser", data.id);
			this.$store.commit("setSid", this.random(40));
			this.$cookies.set("token", data.refresh_token);

			this.makealert(`Logged in as ${data.username}#${data.discriminator}`);

			this.$socket.emit("verifyUser", {
				user: this.$store.state.user,
				sid: this.$store.state.sid,
			});
		},
		callbackValidation(data) {
			if (data.valid) {
				window.localStorage.set("token", data.token);
				const add = "";
				if (this.$route.path !== `/${add}`) {
					this.$route.push({
						path: `/${add}`,
					});
				}
			} else {
				const add = "login/404";
				if (this.$route.path !== `/${add}`) {
					this.$route.push({
						path: `/${add}`,
					});
				}
			}
		},
		playerUpdate(data) {
			console.log(`Recieved:`, "playerUpdate", data);
			this.$store.commit("setInit", data);
			progress.done();
		},
		playPause(data) {
			this.makealert(`Song ${data.state ? "paused" : "resumed"} by: ${data.user}`);
		},
		connect() {
			console.log("Connected to socket!");
			const token = this.$cookies.get("token");
			this.$socket.emit("getUser", {
				refresh_token: token,
			});
			this.$store.commit("switchTab", "queue");
		},
		disconnect() {
			progress.start("page");
		},
	},
	created() {
		window.addEventListener("resize", this.checksize);
	},
	destroyed() {
		window.removeEventListener("resize", this.checksize);
	},
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Rubik&display=swap");

:root {
	--sections: #000b1b;
	--body: #00162a;
	--player-section: #001122;
}

body {
	background: var(--body);
	color: rgb(255, 255, 255);
	font-family: "Rubik", sans-serif;
	user-select: none;
}

.sidepanedivider {
	position: relative;
	top: 60px;
	background: #191944;
	border-color: #191944;
	height: 2px;
	width: 90%;
}

.leftsidebar {
	position: absolute;
	top: 0;
	left: 0;
	width: 375px;
	background: var(--sections);
	height: calc(100% - 100px);
}

.apparea {
	position: absolute;
	top: 0;
	left: 375px;
	width: calc(100% - 375px);
	background: var(--body);
	height: calc(100% - 100px);
}

@media only screen and (max-width: 1300px) {
	.leftsidebar {
		width: 300px;
	}

	.apparea {
		left: 300px;
		width: calc(100% - 300px);
	}
}

.progressing {
	height: 100%;
	position: absolute;
	width: 100%;
	z-index: 10;
	top: 0;
	left: 0;
	background-color: var(--body);
}
::-webkit-scrollbar {
	width: 7px;
	height: 7px;
}

/* Track */
::-webkit-scrollbar-track {
	background: rgb(13 7 43);
	border-radius: 10px;
}

/* Handle */
::-webkit-scrollbar-thumb {
	background: rgb(9 26 58);
	border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
	background: rgb(0 19 56);
}
</style>
