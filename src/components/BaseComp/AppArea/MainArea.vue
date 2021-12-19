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
					}
				"
			>
				<left></left>
			</button>
			<SearchComp ref="search"></SearchComp>
		</div>
		<span class="tabtitle">
			{{ $store.state.tab === "queue" ? "Queue:" : `Showing results for: ${searchinput}` }}
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
						<playicon class="searchresaudiocontrol audiocontrol"></playicon>
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
				:id="queue.indexOf(track)"
				@dragstart="dragstart"
				@dragend="dragend"
				class="searchrestrack draggable"
				:key="queue.indexOf(track)"
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
					<span class="searchresaudiocontrolcontainer" @click="play(track)"
						><playicon class="searchresaudiocontrol"></playicon
					></span>
				</div>
			</div>
		</div>
		<Members></Members>
	</div>
</template>

<script>
import progress from "@/handlers/progress.js";
import playicon from "@/assets/svg/Playicon.vue";
import SearchComp from "@/components/BaseComp/AppArea/SearchComp.vue";
import Members from "@/components/BaseComp/AppArea/Members.vue";
import left from "@/assets/svg/left-arrow.vue";

export default {
	name: "MainArea",
	components: {
		playicon,
		left,
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
			const emitData = {
				song: track,
				guild: this.$store.state.voice.guild,
				channel: this.$store.state.voice.channel,
				user: this.$store.state.user,
			};
			this.$socket.emit("playSongReq", emitData);
			console.log("Emitting:", "playSongReq", emitData);
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

.searchresaudiocontrol {
	fill: white;
	stroke: white;
}
.searchresaudiocontrol:hover {
	cursor: pointer;
}

.searchresaudiocontrol:hover > .playpath {
	stroke: #626ed8;
}
</style>
