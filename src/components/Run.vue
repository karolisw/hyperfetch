<script>

import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles//ag-grid.css";
import "ag-grid-community/styles//ag-theme-alpine.css";
import RunCellRenderer from './renderers/RunCellRenderer.js'

export default {
  name: "Run",
  components: {
    AgGridVue,
    RunCellRenderer
  }, 

  created() { 
    this.currentRun = this.$store.getters.GET_CURRENT_RUN
    this.currentAlg = this.$store.getters.GET_CURRENT_ALG
    this.currentEnv = this.$store.getters.GET_CURRENT_ENV

    // Define grid headers for hyper-parameter grid
    this.columnParams= [
      { headerName: "Param", field: "param", minWidth: 100, cellStyle: {textAlign: 'left'} },
      { headerName: "Value", field: "value",  minWidth: 150, cellStyle: {textAlign: 'left'} },
    ]

    // Define grid headers for stats grid   
    this.columnStats = [
      { headerName: "", field: "", cellRendererSelector: (params) => {
          const envDetails = { component: 'RunCellRenderer' };
          if (params.data.param === 'CO2 emissions' || params.data.param === 'Energy consumed' || params.data.param === 'Total time') return envDetails;
          else return undefined;
        }, minWidth:50, maxWidth: 100 },
      { headerName: "Stats", field: "param", minWidth: 100, maxWidth:200, cellStyle: {textAlign: 'left'}},
      { headerName: "Value", field: "value",  minWidth: 150, cellStyle: {textAlign: 'left'} }, 
    ]

    this.defaultColDef = {
        editable: true,
        sortable: true,
        flex: 1,
        minWidth: 100,
        filter: true,
        resizable: true,
      }
  },

  data() {
    return {
      defaultColDef: null,
      gridApi: null, 
      columnApi: null,
      currentRun: {},
      columnParams: [],
      columnStats: [],
      rowData: [],
      statData: [],
      stats: [],
      currentEnv: "",
      currentAlg: "",
      errorLabel: "",
    };
  },

  methods: {

    /**
     * Grid object is mounted to the DOM and hyper-parameters are loaded into first grid here
     * @param {*} params the current grid 
     */
    onGridReadyHyperparameters(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;

      const updateData = (data) => params.api.setRowData(data);

      // Hyper-parameters are found in the trial parameter of 'currentRun'
      let trial = this.currentRun.trial
      for (const [key, val] of Object.entries(trial)) {
        this.rowData.push({ param: key, value: val })
      }

      updateData(this.rowData)
    },

    
    /**
     * Grid object is mounted to the DOM and stats are loaded into second grid here
     * @param {*} params the current grid 
     */
    onGridReadyStats(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi; 

      const updateData = (data) => {
        params.api.setRowData(data)
      };
      
      let run = this.currentRun
      this.statData.push({ param: "CO2 emissions", value: run.CO2_emissions })
      this.statData.push({ param: "Energy consumed", value: run.energy_consumed })
      this.statData.push({ param: "Total time", value: run.total_time })
      this.statData.push({ param: "Reward", value: run.reward }) 
      this.statData.push({ param: "CPU model", value: run.cpu_model })
      this.statData.push({ param: "GPU model", value: run.gpu_model })
      this.statData.push({ param: "Project name", value: run.project_name })
      this.statData.push({ param: "Git link", value: run.git_link })

      updateData(this.statData)
    }
  }
}
</script>

<template>  
  <div>
    <div class="run-stats">
      <h3>Step 3: View stats for run</h3>
      <ag-grid-vue id="stats"
        @grid-ready="onGridReadyStats"
        style="width: 80vh; height: 40vh"
        class="ag-theme-alpine"
        :defaultColDef="defaultColDef"
        :columnDefs="columnStats"
        :rowData="statData">
      </ag-grid-vue>
    </div>

    <div class="run-hyperparameters">
      <h3>Step 4: View hyperparameters for run</h3>
      <ag-grid-vue id="hyperparameters"
      @grid-ready="onGridReadyHyperparameters"
      style="width: 80vh; height: 60vh"
      class="ag-theme-alpine"
      :defaultColDef="defaultColDef"
      :columnDefs="columnParams"
      :rowData="rowData">
      </ag-grid-vue>
    </div>
  </div>
</template>


<style lang="scss" scoped>
.ag-theme-alpine {
  --ag-secondary-border-color: none;
  --ag-font-size: 15px;

}

.run-stats {
  margin-top: 5%;
  margin-bottom: 3%;
}

#hyperparameters {
  margin-bottom: 10vh;
}

.run-stats, #stats {
  --ag-foreground-color: rgb(57, 59, 51);
  --ag-background-color: rgb(255, 237, 184);
  --ag-header-foreground-color: rgb(57, 59, 51);
  --ag-header-background-color: rgb(253, 222, 142);
  --ag-odd-row-background-color: rgb(0, 0, 0, 0.03);
  --ag-header-column-resize-handle-color: rgb(74, 74, 224);
}

.ag-theme-alpine, #hyperparameters {
  --ag-border-color:rgb(57, 59, 51);
  --ag-foreground-color: rgb(57, 59, 51);
  --ag-background-color: rgb(255, 223, 209);
  --ag-header-foreground-color: rgb(57, 59, 51);
  --ag-header-background-color: rgb(255, 204, 172);
  --ag-odd-row-background-color: rgb(0, 0, 0, 0.03);
  --ag-header-column-resize-handle-color: rgb(74, 74, 224);
}
</style>
