<template>
	<div>
		<el-row :gutter="20">
			<el-col :span="8">
				<div class="panel">
					<panel-title :title="$lang.objects.client">
						<el-button size="mini" type="primary">
							{{ $lang.buttons.normal }}
						</el-button>
					</panel-title>
					<div v-loading="loading" class="panel-body">
						<h1 class="number">{{ status.success }}</h1>
						<small> {{ $lang.descriptions.normalClients }}</small>
					</div>
				</div>
			</el-col>
			<el-col :span="8">
				<div class="panel">
					<panel-title :title="$lang.objects.client">
						<el-button size="mini" type="danger">
							{{ $lang.buttons.error }}
						</el-button>
					</panel-title>
					<div v-loading="loading" class="panel-body">
						<h1 class="number">{{ status.error }}</h1>
						<small> {{ $lang.descriptions.errorClients }}</small>
					</div>
				</div>
			</el-col>
			<el-col :span="8">
				<div id="tree" class="panel">
					<panel-title :title="$lang.objects.project">
						<el-button size="mini" type="success">
							{{ $lang.buttons.normal }}
						</el-button>
					</panel-title>
					<div v-loading="loading" class="panel-body">
						<h1 class="number">{{ status.project }}</h1>
						<small>{{ $lang.descriptions.countProjects }}</small>
					</div>
				</div>
			</el-col>
		</el-row>
		<el-row :gutter="20" v-if="host_infos">
			<el-col :span="8" v-for="host_info in host_infos" :key="host_info.title">
				<div id="tree" class="panel">
					<panel-title :title="host_info.title"></panel-title>
					<div v-loading="loading" class="panel-body">
						<div class="grid_body">
							<small>{{ host_info.first.name }}</small>
							<el-progress :percentage="host_info.first.data" text-inside :stroke-width="20"></el-progress>
						</div>
						<div class="grid_body">
							<small>{{ host_info.second.name }}</small>
							<el-progress :percentage="host_info.second.data" text-inside :stroke-width="20"></el-progress>
						</div>
						<div class="grid_body">
							<small>{{ host_info.three.name }}</small>
							<el-progress :percentage="host_info.three.data" text-inside :stroke-width="20"></el-progress>
						</div>
						<div class="grid_body">
							<small>{{ host_info.four.name }}</small>
							<div>
								<el-tag style="line-height: 20px; height: 20px;">{{ host_info.four.data }}</el-tag>
							</div>
						</div>
						<div class="grid_body">
							<small>{{ host_info.five.name }}</small>
							<div>
								<el-tag style="line-height: 20px; height: 20px;">{{ host_info.five.data }}</el-tag>
							</div>
						</div>
					</div>
				</div>
			</el-col>
		</el-row>
	</div>
</template>
<script>
import PanelTitle from "../../components/PanelTitle";

export default {
	data() {
		return {
			radio: "1",
			status: {},
			host_infos: null,
			loading: true,
			timer: null,
			intervalTime: 5000,
		};
	},
	components: {
		// ElFormItem,
		PanelTitle,
	},
	created() {
		this.getHomeStatus();
		this.setupTimer();
	},
	mounted() {
		this.getHostInfosData();
	},
	methods: {
		getHomeStatus() {
			this.$http
				.get(this.$store.state.url.home.status)
				.then(({data: status}) => {
					this.status = status;
					this.loading = false;
				});
		},
		getHostInfosData() {
			this.$http
				.get(this.$store.state.url.home.hostInfos)
				.then(({data: data}) => {
					this.host_infos = data['host_infos'];
				});
		},
		setupTimer() {
			this.timer = setTimeout(() => {
				this.getHostInfosData();
				this.setupTimer();
			}, this.intervalTime);
		}
	},
	beforeDestroy() {
		if (this.timer) {
			clearTimeout(this.timer);
		}
	},
};
</script>

<style scoped>
h1.number {
	font-weight: 100;
	margin: 10px 0;
	margin-top: 0;
}

.grid_body {
	display: grid;
	grid-template-columns: 2fr 8fr; /* 两列等宽 */
	margin: 10px 0;
}

.grid_body small {
	text-align: right;
	margin-right: 20px;
}
</style>
