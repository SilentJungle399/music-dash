<template>
	<div class="barcontainer">
		<div @click="seek" class="bar">
			<div class="progress" :style="`width: ${progress}%`"></div>
			<div id="peg" class="progresshandle" :style="`left: ${progress}%; opacity: ${show ? 1 : 0}`"></div>
		</div>
	</div>
</template>

<script>
export default {
	name: "SeekBar",
	data() {
		return {
		};
	},
	methods: {
	},
};
</script>

<style>
.bar {
	background: #333;
	user-select: none;

	position: fixed;
	z-index: 1;
	bottom: 80px;
	left: 0;
	padding: 1px;

	width: 100%;
	height: 2px;
}

.bar:hover {
	cursor: pointer;
}

.progresshandle {
	user-select: none;
	display: block;
	position: absolute;
	z-index: 2;
	margin-top: -8px;
	margin-left: -10px;
	width: 10px;
	opacity: 0;
	transition: opacity 0.5s;
	height: 10px;
	border: 4px solid red;
	border-top-color: red;
	border-right-color: red;
	border-radius: 100%;
	background-color: red;
	box-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
	cursor: pointer;
}

.progress {
	background: red;

	position: fixed;
	z-index: 1;
	bottom: 80px;
	left: 0;
	padding: 1px;

	height: 2px;
}
</style>
