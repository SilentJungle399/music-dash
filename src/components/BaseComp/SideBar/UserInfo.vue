<template>
	<div class="UserInfo">
		<table class="UserInfotable">
			<tr>
				<td rowspan="2">
					<img
						:src="
							$store.state.voice.guild.icon
								? $store.state.voice.guild.icon
								: 'https://cdn.discordapp.com/icons/526000157620437014/05c5487e54b4623a129134e121e05636.webp'
						"
						class="userpfp"
						alt=""
					/>
				</td>
				<td class="tdalign">
					<span class="username">{{
						$store.state.voice.guild.name
							? $store.state.voice.guild.name
							: "Not connected"
					}}</span>
				</td>
			</tr>
			<tr>
				<td class="tdalign">
					<span class="discrim"
						>#{{
							$store.state.voice.channel.name
								? $store.state.voice.channel.name.length > 10
									? $store.state.voice.channel.name.substring(0, 15) + "..."
									: $store.state.voice.channel.name
								: "invalid-channel "
						}}</span
					>
				</td>
			</tr>
		</table>
	</div>
</template>

<script>
import progress from "@/handlers/progress.js";

export default {
	name: "UserInfo",
};
</script>

<style>
/* .UserInfo {
	background-color: var(--sections);
	position: absolute;
	display: flex;
	top: 0;
	left: 0;
	width: 375px;
	height: 100px;
} */

.UserInfo {
	position: relative;
	top: 20px;
	height: 50px;
	color: white;
	display: flex;
	text-align: center;
}

.tdalign {
	text-align: left;
}

/* .userpfp {
	height: 40px;
	position: relative;
	left: 8px;
	border-radius: 50%;
	top: 5px;
}

.username {
	font-size: 17px;
	position: relative;
	color: #fff;
} */

/* ------------------------------------------- */

.userpfp {
	height: 75px;
	border-radius: 50%;
}

.discrim {
	padding-left: 15px;
	position: relative;
	color: #ffffffc4;
	bottom: 20px;
	font-size: 15px;
}

.username {
	padding-left: 15px;
	font-size: 17px;
	position: relative;
	bottom: 5px;
}

.UserInfotable {
	margin: auto;
}
</style>
