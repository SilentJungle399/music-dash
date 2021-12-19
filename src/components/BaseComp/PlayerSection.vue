<template>
	<div class="playersection">
		<SeekBar :draggable="true"></SeekBar>
		<div class="songdata" v-if="$store.state.player.track">
			<table cellspacing="0">
				<tr>
					<td rowspan="2">
						<img
							:src="`https://img.youtube.com/vi/${$store.state.player.track.info.identifier}/0.jpg`"
							alt="yt thumbnail"
							class="currentthumbnail"
						/>
					</td>
					<td>
						<span class="currentsongname">
							{{
								$store.state.player.track.info.title.length > 40
									? $store.state.player.track.info.title.substring(0, 40) + "..."
									: $store.state.player.track.info.title
							}}
						</span>
						<br />
					</td>
				</tr>
				<tr>
					<td>
						<span class="currentsongchannel">{{
							$store.state.player.track.info.author
						}}</span>
					</td>
				</tr>
			</table>
		</div>
		<div class="controls">
			<!-- prettier-ignore -->
			<span
				class="controlbutton"
				@click="() => {$store.commit('togRepeat');}"
			>
				<repeaticon></repeaticon
			></span>
			<span class="controlbutton" @click="ff(-10)">
				<backw class="audiocontrol"></backw>
			</span>
			<span class="controlbutton" @click="skip(false)">
				<SkipPrevious class="audiocontrol"></SkipPrevious>
			</span>
			<span
				class="controlbutton"
				@click="playpause"
				v-if="$store.state.player.track ? $store.state.player.paused : true"
			>
				<playicon class="audiocontrol"></playicon>
			</span>
			<span class="controlbutton" @click="playpause" v-else>
				<pauseicon class="audiocontrol"></pauseicon>
			</span>
			<span class="controlbutton" @click="skip(true)">
				<SkipNext class="audiocontrol"></SkipNext>
			</span>
			<span class="controlbutton" @click="ff(10)">
				<forw class="audiocontrol"></forw>
			</span>
			<!-- prettier-ignore -->
			<span
				class="controlbutton"
				@click="() => {$store.commit('togShuffle');}"
			>
				<shuffleicon></shuffleicon>
			</span>
		</div>
		<!-- <div class="extrabuttons">
			<span class="controlbutton" @mouseenter="discordHover(true)" @mouseleave="discordHover(false)" v-if="$store.state.members.length > 0">
				<discord class="audiocontrol"></discord>
			</span>
		</div> -->
	</div>
</template>

<script>
import playicon from "@/assets/svg/Playicon.vue";
import repeaticon from "@/assets/svg/Repeaticon.vue";
import shuffleicon from "@/assets/svg/Shuffleicon.vue";
import pauseicon from "@/assets/svg/Pauseicon.vue";
import SeekBar from "@/components/utils/SeekBar.vue";
import SkipNext from "@/assets/svg/SkipNext.vue";
import SkipPrevious from "@/assets/svg/SkipPrevious.vue";
import forw from "@/assets/svg/forw.vue";
import backw from "@/assets/svg/backw.vue";
import discord from "@/assets/svg/discord.vue";

export default {
	name: "PlayerSection",
	props: {
		preTrack: {
			required: true,
		},
	},
	components: {
		playicon,
		repeaticon,
		shuffleicon,
		pauseicon,
		SeekBar,
		SkipNext,
		SkipPrevious,
		forw,
		backw,
		discord,
	},
	data() {
		return {
			player: {
				paused: true,
				seekable: false,
			},
			barInterval: null,
			seekable: false,
		};
	},
	mounted() {},
	methods: {
		discordHover(state) {
			const elem = document.getElementById("membersdiv");
			elem.style.opacity = state ? "1" : "0";
			elem.style.bottom = state ? "0" : "-10%";
		},
		ff(dir) {
			const emitData = {
				ff: dir,
				guild: this.$store.state.voice.guild,
				channel: this.$store.state.voice.channel,
				user: this.$store.state.user,
			};
			this.$socket.emit("FastForwardReq", emitData);
			console.log("Emitting:", "FastForwardReq", emitData);
		},
		skip() {},
		playpause() {
			const emitData = {
				guild: this.$store.state.voice.guild,
				channel: this.$store.state.voice.channel,
				user: this.$store.state.user,
				state: !this.$store.state.player.paused,
			};
			this.$socket.emit("PlayPauseReq", emitData);
			console.log("Emitting:", "PlayPauseReq", emitData);
		},
	},
	sockets: {
		TrackStart(data) {
			console.log("Received: ", "TrackStart", data);
			this.$store.commit("setTrack", data.track);
		},
		TrackEnd(data) {
			console.log("Received: ", "TrackEnd", data);
			this.$store.commit("setProgress", 0);
			this.$store.commit("setTrack", null);
		},
		playPause(data) {
			console.log("Received: ", "playPause", data);
			this.$store.commit("setPaused", data.state);
		},
	},
};
</script>

<style>
.currentsongname {
	position: relative;
	padding-left: 10px;
}
.currentsongchannel {
	position: relative;
	padding-left: 10px;
	bottom: 20px;
	color: #ffffff54;
}

.songdata {
	position: absolute;
	bottom: 10px;
	left: 0;
}

.currentthumbnail {
	height: 70px;
	margin-left: 30px;
	margin-top: 5px;
}

.playersection {
	background-color: var(--player-section);
	position: absolute;
	display: flex;
	bottom: 0;
	left: 0;
	right: 0;
	width: 100%;
	height: 100px;
}

.controls {
	margin: auto;
	display: flex;
}

.audiocontrol {
	padding: 10px;
	fill: white;
	transition: all 0.5s;
}

.controlbutton {
	border-radius: 50px;
	transition: all 0.25s;
	font-size: 0;
}

.controlbutton:hover {
	background: #18162b;
	cursor: pointer;
}

.extrabuttons {
	position: absolute;
	bottom: 30px;
	right: 20px;
	margin: auto;
	display: flex;
}
</style>
