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
			<span
				class="controlbutton"
				@click="
					() => {
						$store.commit('togRepeat');
					}
				"
			>
				<div>
					<svg
						class="audiocontrol"
						v-if="!$store.state.player.controls.repeat"
						xmlns="http://www.w3.org/2000/svg"
						height="24px"
						viewBox="0 0 24 24"
						width="24px"
					>
						<path
							d="M7 7h10v1.79c0 .45.54.67.85.35l2.79-2.79c.2-.2.2-.51 0-.71l-2.79-2.79c-.31-.31-.85-.09-.85.36V5H6c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1s1-.45 1-1V7zm10 10H7v-1.79c0-.45-.54-.67-.85-.35l-2.79 2.79c-.2.2-.2.51 0 .71l2.79 2.79c.31.31.85.09.85-.36V19h11c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1s-1 .45-1 1v3z"
						/>
					</svg>
					<svg
						class="audiocontrol"
						v-else
						xmlns="http://www.w3.org/2000/svg"
						enable-background="new 0 0 24 24"
						height="24px"
						viewBox="0 0 24 24"
						width="24px"
						style="stroke: white"
					>
						<path
							d="M7 7h10v1.79c0 .45.54.67.85.35l2.79-2.79c.2-.2.2-.51 0-.71l-2.79-2.79c-.31-.31-.85-.09-.85.36V5H6c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1s1-.45 1-1V7zm10 10H7v-1.79c0-.45-.54-.67-.85-.35l-2.79 2.79c-.2.2-.2.51 0 .71l2.79 2.79c.31.31.85.09.85-.36V19h11c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1s-1 .45-1 1v3z"
						/>
					</svg>
				</div>
				></span
			>
			<span class="controlbutton" @click="ff(-10)">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24px"
					viewBox="0 0 24 24"
					width="24px"
					fill="#000000"
				>
					<path
						d="M11.99 5V1l-5 5 5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6h-2c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8zm-1.1 11h-.85v-3.26l-1.01.31v-.69l1.77-.63h.09V16zm4.28-1.76c0 .32-.03.6-.1.82s-.17.42-.29.57-.28.26-.45.33-.37.1-.59.1-.41-.03-.59-.1-.33-.18-.46-.33-.23-.34-.3-.57-.11-.5-.11-.82v-.74c0-.32.03-.6.1-.82s.17-.42.29-.57.28-.26.45-.33.37-.1.59-.1.41.03.59.1.33.18.46.33.23.34.3.57.11.5.11.82v.74zm-.85-.86c0-.19-.01-.35-.04-.48s-.07-.23-.12-.31-.11-.14-.19-.17-.16-.05-.25-.05-.18.02-.25.05-.14.09-.19.17-.09.18-.12.31-.04.29-.04.48v.97c0 .19.01.35.04.48s.07.24.12.32.11.14.19.17.16.05.25.05.18-.02.25-.05.14-.09.19-.17.09-.19.11-.32.04-.29.04-.48v-.97z"
					/>
				</svg>
			</span>
			<span class="controlbutton" @click="skip(false)">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24px"
					viewBox="0 0 24 24"
					width="24px"
				>
					<path
						d="M7 6c.55 0 1 .45 1 1v10c0 .55-.45 1-1 1s-1-.45-1-1V7c0-.55.45-1 1-1zm3.66 6.82l5.77 4.07c.66.47 1.58-.01 1.58-.82V7.93c0-.81-.91-1.28-1.58-.82l-5.77 4.07c-.57.4-.57 1.24 0 1.64z"
					/>
				</svg>
			</span>
			<span
				class="controlbutton"
				@click="playpause"
				v-if="$store.state.player.track ? $store.state.player.paused : true"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24px"
					viewBox="0 0 24 24"
					width="24px"
				>
					<path
						d="M8 6.82v10.36c0 .79.87 1.27 1.54.84l8.14-5.18c.62-.39.62-1.29 0-1.69L9.54 5.98C8.87 5.55 8 6.03 8 6.82z"
					/>
				</svg>
			</span>
			<span class="controlbutton" @click="playpause" v-else>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24px"
					viewBox="0 0 24 24"
					width="24px"
				>
					<path
						d="M8 19c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2s-2 .9-2 2v10c0 1.1.9 2 2 2zm6-12v10c0 1.1.9 2 2 2s2-.9 2-2V7c0-1.1-.9-2-2-2s-2 .9-2 2z"
					/>
				</svg>
			</span>
			<span class="controlbutton" @click="skip(true)">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24px"
					viewBox="0 0 24 24"
					width="24px"
				>
					<path
						d="M7.58 16.89l5.77-4.07c.56-.4.56-1.24 0-1.63L7.58 7.11C6.91 6.65 6 7.12 6 7.93v8.14c0 .81.91 1.28 1.58.82zM16 7v10c0 .55.45 1 1 1s1-.45 1-1V7c0-.55-.45-1-1-1s-1 .45-1 1z"
					/>
				</svg>
			</span>
			<span class="controlbutton" @click="ff(10)">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					enable-background="new 0 0 24 24"
					height="24px"
					viewBox="0 0 24 24"
					width="24px"
					fill="#000000"
				>
					<g>
						<g />
						<g>
							<path
								d="M18,13c0,3.31-2.69,6-6,6s-6-2.69-6-6s2.69-6,6-6v4l5-5l-5-5v4c-4.42,0-8,3.58-8,8c0,4.42,3.58,8,8,8s8-3.58,8-8H18z"
							/>
							<polygon
								points="10.9,16 10.9,11.73 10.81,11.73 9.04,12.36 9.04,13.05 10.05,12.74 10.05,16"
							/>
							<path
								d="M14.32,11.78c-0.18-0.07-0.37-0.1-0.59-0.1s-0.41,0.03-0.59,0.1s-0.33,0.18-0.45,0.33s-0.23,0.34-0.29,0.57 s-0.1,0.5-0.1,0.82v0.74c0,0.32,0.04,0.6,0.11,0.82s0.17,0.42,0.3,0.57s0.28,0.26,0.46,0.33s0.37,0.1,0.59,0.1s0.41-0.03,0.59-0.1 s0.33-0.18,0.45-0.33s0.22-0.34,0.29-0.57s0.1-0.5,0.1-0.82V13.5c0-0.32-0.04-0.6-0.11-0.82s-0.17-0.42-0.3-0.57 S14.49,11.85,14.32,11.78z M14.33,14.35c0,0.19-0.01,0.35-0.04,0.48s-0.06,0.24-0.11,0.32s-0.11,0.14-0.19,0.17 s-0.16,0.05-0.25,0.05s-0.18-0.02-0.25-0.05s-0.14-0.09-0.19-0.17s-0.09-0.19-0.12-0.32s-0.04-0.29-0.04-0.48v-0.97 c0-0.19,0.01-0.35,0.04-0.48s0.06-0.23,0.12-0.31s0.11-0.14,0.19-0.17s0.16-0.05,0.25-0.05s0.18,0.02,0.25,0.05 s0.14,0.09,0.19,0.17s0.09,0.18,0.12,0.31s0.04,0.29,0.04,0.48V14.35z"
							/>
						</g>
					</g>
				</svg>
			</span>
			<!-- prettier-ignore -->
			<span
				class="controlbutton"
				@click="() => {$store.commit('togShuffle');}"
			>
	<svg
		class="audiocontrol"
		xmlns="http://www.w3.org/2000/svg"
		height="24px"
		viewBox="0 0 24 24"
		width="24px"
		:style="$store.state.player.controls.shuffle ? 'stroke: white' : ''"
	>
		<path
			d="M10.59 9.17L6.12 4.7c-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41l4.46 4.46 1.42-1.4zm4.76-4.32l1.19 1.19L4.7 17.88c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0L17.96 7.46l1.19 1.19c.31.31.85.09.85-.36V4.5c0-.28-.22-.5-.5-.5h-3.79c-.45 0-.67.54-.36.85zm-.52 8.56l-1.41 1.41 3.13 3.13-1.2 1.2c-.31.31-.09.85.36.85h3.79c.28 0 .5-.22.5-.5v-3.79c0-.45-.54-.67-.85-.35l-1.19 1.19-3.13-3.14z"
		/>
	</svg>
			</span>
		</div>
		<!-- <div class="extrabuttons">
			<span
				class="controlbutton"
				@mouseenter="discordHover(true)"
				@mouseleave="discordHover(false)"
				v-if="$store.state.members.length > 0"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					enable-background="new 0 0 24 24"
					height="24px"
					viewBox="0 0 24 24"
					width="24px"
					fill="#000000"
				>
					<g>
						<path
							d="M4,13c1.1,0,2-0.9,2-2c0-1.1-0.9-2-2-2s-2,0.9-2,2C2,12.1,2.9,13,4,13z M5.13,14.1C4.76,14.04,4.39,14,4,14 c-0.99,0-1.93,0.21-2.78,0.58C0.48,14.9,0,15.62,0,16.43V18l4.5,0v-1.61C4.5,15.56,4.73,14.78,5.13,14.1z M20,13c1.1,0,2-0.9,2-2 c0-1.1-0.9-2-2-2s-2,0.9-2,2C18,12.1,18.9,13,20,13z M24,16.43c0-0.81-0.48-1.53-1.22-1.85C21.93,14.21,20.99,14,20,14 c-0.39,0-0.76,0.04-1.13,0.1c0.4,0.68,0.63,1.46,0.63,2.29V18l4.5,0V16.43z M16.24,13.65c-1.17-0.52-2.61-0.9-4.24-0.9 c-1.63,0-3.07,0.39-4.24,0.9C6.68,14.13,6,15.21,6,16.39V18h12v-1.61C18,15.21,17.32,14.13,16.24,13.65z M8.07,16 c0.09-0.23,0.13-0.39,0.91-0.69c0.97-0.38,1.99-0.56,3.02-0.56s2.05,0.18,3.02,0.56c0.77,0.3,0.81,0.46,0.91,0.69H8.07z M12,8 c0.55,0,1,0.45,1,1s-0.45,1-1,1s-1-0.45-1-1S11.45,8,12,8 M12,6c-1.66,0-3,1.34-3,3c0,1.66,1.34,3,3,3s3-1.34,3-3 C15,7.34,13.66,6,12,6L12,6z"
						/>
					</g>
				</svg>
			</span>
		</div> -->
	</div>
</template>

<script>
import SeekBar from "@/components/utils/SeekBar.vue";

export default {
	name: "PlayerSection",
	props: {
		preTrack: {
			required: true,
		},
	},
	components: {
		SeekBar,
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
			if (!this.$store.state.voice.guild.id) {
				return this.$emit("makealert", "You are not in a voice channel.");
			} else if (!this.$store.state.player.track) {
				return this.$emit("makealert", "There is no current song.");
			}
			const emitData = {
				ff: dir,
				guild: this.$store.state.voice.guild,
				channel: this.$store.state.voice.channel,
				user: this.$store.state.user,
			};
			this.$socket.emit("FastForwardReq", emitData);
			console.log("Emitting:", "FastForwardReq", emitData);
		},
		skip(state) {
			if (!this.$store.state.voice.guild.id) {
				return this.$emit("makealert", "You are not in a voice channel.");
			} else if (!this.$store.state.player.track) {
				return this.$emit(
					"makealert",
					state ? "The queue is empty." : "There is no current song."
				);
			}
			const emitData = {
				progress: state ? 100 : 0,
				guild: this.$store.state.voice.guild,
				channel: this.$store.state.voice.channel,
			};
			this.$socket.emit("seek", emitData);
			console.log("Emitting:", "seek", emitData);
		},
		playpause() {
			if (!this.$store.state.voice.guild.id) {
				return this.$emit("makealert", "You are not in a voice channel.");
			} else if (!this.$store.state.player.track) {
				return this.$emit("makealert", "There is no current song.");
			}
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
		newQueue(data) {
			console.log("Received: ", "newQueue", data);
			this.$store.commit("setQueue", data.queue);
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

svg {
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
