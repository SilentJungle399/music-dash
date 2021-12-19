<template>
	<div class="mainarea">
		<div class="headercont">
			<button
				class="backbutton"
				v-if="$store.state.tab !== 'queue'"
				@click="
					() => {
						$store.commit('switchTab', 'queue');
						searchres = [];
						$refs.search.searchinput = null;
					}
				"
			>
				<svg
					width="20"
					height="20"
					viewBox="0 0 20 20"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M2.29289 9.29289C1.90237 9.68342 1.90237 10.3166 2.29289 10.7071L8.65685 17.0711C9.04738 17.4616 9.68054 17.4616 10.0711 17.0711C10.4616 16.6805 10.4616 16.0474 10.0711 15.6569L4.41421 10L10.0711 4.34315C10.4616 3.95262 10.4616 3.31946 10.0711 2.92893C9.68054 2.53841 9.04738 2.53841 8.65685 2.92893L2.29289 9.29289ZM15 9L3 9V11L15 11V9Z"
						fill="white"
					/>
				</svg>
			</button>
			<SearchComp ref="search"></SearchComp>
		</div>
		<span class="tabtitle">
			{{
				$store.state.tab === "queue"
					? $store.state.queue.length > 0
						? "Queue:"
						: "The queue is empty!"
					: `Showing results for: ${searchinput}`
			}}
			<br />
		</span>
		<div
			class="scrollarea"
			style="width: 100%; top: 120px"
			v-if="$store.state.tab === 'search'"
		>
			<div class="searchrestrack" :key="searchres.indexOf(track)" v-for="track in searchres">
				<img
					:src="`https://img.youtube.com/vi/${track.info.identifier}/0.jpg`"
					alt=""
					class="searchresthumbnail"
				/>
				<div class="songdiv">
					<span class="searchresinfoname">{{ track.info.title }}</span>
					<span class="searchresinfochannel">{{ track.info.author }}</span>
				</div>
				<div class="searchrescontrols">
					<span class="searchresaudiocontrolcontainer" @click="play(track)">
						<svg
							class="trackcontrol"
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
				</div>
			</div>
		</div>
		<div
			class="scrollarea"
			style="width: 100%; top: 120px"
			v-else-if="$store.state.tab === 'queue'"
		>
			<div
				:id="$store.state.queue.indexOf(track)"
				class="searchrestrack draggable"
				:key="$store.state.queue.indexOf(track)"
				v-for="track in $store.state.queue"
				draggable="true"
			>
				<img
					:src="`https://img.youtube.com/vi/${track.info.identifier}/0.jpg`"
					alt=""
					class="searchresthumbnail"
				/>

				<div class="songdiv">
					<span class="searchresinfoname">{{ track.info.title }}</span>
					<span class="searchresinfochannel">{{ track.info.author }}</span>
				</div>
				<div class="searchrescontrols">
					<span
						class="searchresaudiocontrolcontainer"
						@click="removeSong($store.state.queue.indexOf(track))"
					>
						<svg
							class="trackcontrol"
							xmlns="http://www.w3.org/2000/svg"
							height="24px"
							viewBox="0 0 24 24"
							width="24px"
							fill="#000000"
							style="stroke-width: 0.4px"
						>
							<path
								d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-3.5l-1-1zM18 7H6v12c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7z"
							/></svg
					></span>
				</div>
			</div>
		</div>
		<Members></Members>
	</div>
</template>

<script>
import progress from "@/handlers/progress.js";
import SearchComp from "@/components/BaseComp/AppArea/SearchComp.vue";
import Members from "@/components/BaseComp/AppArea/Members.vue";

export default {
	name: "MainArea",
	components: {
		SearchComp,
		Members,
	},
	data() {
		return {
			tab: "queue",
			searchres: [],
			dragactive: false,
			dragpos: null,
			curdrag: null,
			newpos: null,
			searchinput: null,
		};
	},
	methods: {
		play(track) {
			if (!this.$store.state.voice.guild.id) {
				return this.$emit("makealert", "You are not in a voice channel.");
			}
			const emitData = {
				song: track,
				guild: this.$store.state.voice.guild,
				channel: this.$store.state.voice.channel,
				user: this.$store.state.user,
			};
			this.$socket.emit("playSongReq", emitData);
			console.log("Emitting:", "playSongReq", emitData);
		},
		removeSong(track) {
			if (!this.$store.state.voice.guild.id) {
				return this.$emit("makealert", "You are not in a voice channel.");
			}
			const emitData = {
				song: track,
				guild: this.$store.state.voice.guild,
				channel: this.$store.state.voice.channel,
				user: this.$store.state.user,
			};
			this.$socket.emit("removeSong", emitData);
			console.log("Emitting:", "removeSong", emitData);
		},
	},
	sockets: {
		songResult(data) {
			console.log("Received: ", "songResult", data);
			this.searchres = data.songs;
			this.searchinput = data.keyword;
			this.$store.commit("switchTab", "search");
		},
	},
};
</script>

<style>
/* .mainarea {
	background-color: var(--sections);
	position: absolute;
	top: 125px;
	display: flex;
	padding: 50px 30px 30px 30px;
	right: 0;
	width: calc(100% - 435px - 25px);
	height: calc(100% - 310px);
	border-radius: 50px 0 0 0;
} */

.scrollarea {
	overflow-y: auto;
	top: 140px;
	position: absolute;
	bottom: 20px;
	right: 0;
}

.tabtitle {
	position: absolute;
	top: 80px;
	left: 30px;
	font-size: 20px;
	color: #cecece;
}

.headercont {
	display: flex;
	position: absolute;
	top: 0;
	left: 0;
	flex-direction: row;
	width: 100%;
	align-content: center;
	justify-content: center;
	align-items: center;
}

.draggable {
	cursor: grab;
}

.dragging {
	cursor: grabbing;
}

.backbutton {
	background: none;
	outline: none;
	border: none;
	color: white;
	border-radius: 62px;
	padding: 10px;
	padding-bottom: 7px;
	transition: all 0.5s;
	margin-left: 20px;
}

.backbutton:hover {
	background: #1c172f;
	cursor: pointer;
}

.searchresthumbnail {
	height: 100px;
}

.searchresinfochannel {
	color: #ffffffc4;
}

.songdiv {
	display: flex;
	padding: 10px;
	flex-direction: column;
}

.searchrestrack {
	padding: 10px 10px 10px 20px;
	border-radius: 10px;
	transition: background 0.5s;
	margin: 10px;
	display: flex;
}

.searchrescontrols {
	margin: auto 50px auto auto;
	opacity: 0;
	transition: opacity 0.5s;
}

.searchrestrack:hover {
	background: #18162b;
}

.searchrestrack:hover > .searchrescontrols {
	opacity: 1;
}

.playpath {
	transition: stroke 0.5s;
}

.trackcontrol {
	fill: white;
	stroke: white;
}
.trackcontrol:hover {
	cursor: pointer;
}

.searchresaudiocontrol:hover > .playpath {
	stroke: #626ed8;
}
</style>
