module.exports = {
	productionSourceMap: false,
	devServer: {
		host: "0.0.0.0",
		disableHostCheck: true,
		proxy: {
			"/socket.io": {
				target: "http://localhost:3000",
			},
			"/callback": {
				target: "http://localhost:3000",
			},
			"/verify": {
				target: "http://localhost:3000",
			},
		},
	},
};
