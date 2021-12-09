import Vue from "vue";
import App from "./App.vue";
import io from "socket.io-client";
import VueSocketIO from "vue-socket.io";
import NProgress from "nprogress";
import store from "./handlers/store";

Vue.use(
	new VueSocketIO({
		connection: io("http://localhost:3000"),
	})
);

Vue.config.productionTip = false;

NProgress.start();

new Vue({
	render: (h) => h(App),
	store: store,
}).$mount("#app");
