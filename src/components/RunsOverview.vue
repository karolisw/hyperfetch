<script>

import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles//ag-grid.css";
import "ag-grid-community/styles//ag-theme-alpine.css";

export default {
  name: "RunsOverview",
  emits: ["selectedRun"],
  components: {
    AgGridVue
  }, 


  created() { 
    // Only one row can be selected at a time from grid
    this.rowSelection = 'single';
    this.currentEnv = this.$store.getters.GET_CURRENT_ENV
    this.currentAlg = this.$store.getters.GET_CURRENT_ALG
    this.runs = this.$store.getters.GET_RUNS

    // Define grid headers
    this.columnDefs= [
        { headerName: "ID", field: "id", minWidth: 50, maxWidth: 200},
        { headerName: "Reward", field: "reward",  minWidth: 100, maxWidth:130 },
        { headerName: "Energy Usage (kWh)", field: "energy",  minWidth: 100, maxWidth: 180 },  
        { headerName: "Emissions (kg CO2)", field: "co2",  minWidth: 100, maxWidth: 180 },  
      ]

      this.defaultColDef = {
        editable: false,
        sortable: true,
        flex: 1,
        minWidth: 100,
        filter: true,
        resizable: true,
      }
  },

  data() {
    return {
        gridApi: null, 
        columnApi: null,
        defaultColDef: null,
        runs: [], 
        columnDefs: [],
        rowData: [],
        rowSelection: null,
        currentEnv: "",
        currentAlg: "",
        errorLabel: "",
    };
  },

  methods: {
    async onSelectRun() { 
        const selectedRows = this.gridApi.getSelectedRows() 
        
        document.querySelector('#selectedRows2').innerHTML = selectedRows.length === 1 ? selectedRows[0].id : ''

        // Fetch the run
        await this.$store.dispatch('getRun', {id: selectedRows[0].id})

        //document.getElementById("selectedRows2").style.visibility = "hidden"; 

        console.log("CURRENT RUN: ", this.$store.getters.GET_CURRENT_RUN)
        // Telling the parent of this component that an algorithm has been selected and that runs can be shown
        this.$emit("selectedRun", this.$store.getters.GET_CURRENT_RUN) 
    }, 

    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;

      const updateData = (data) => params.api.setRowData(data);

      // Retrieve the necessary data from runs and convert each run to a row
      for (let i = 0; i < this.runs.length; i++) {
        const element = this.runs[i]
        this.rowData.push({ 
          id: element.run_id, 
          reward: element.reward, 
          energy: element.energy_consumed, 
          co2: element.CO2_emissions
        })
      }

      updateData(this.rowData)
    },
  }
}
</script>

<template>  
<div id="selectedRows2">
  <h3>Step 2: Select a run</h3>
  <ag-grid-vue 
  @grid-ready="onGridReady"
  @selection-changed="onSelectRun"
  style="width: 692px; height: 400px"
  class="ag-theme-alpine"
  :defaultColDef="defaultColDef"
  :rowSelection="rowSelection"
  :columnDefs="columnDefs"
  :rowData="rowData">
  </ag-grid-vue>
</div>

</template>

<style scss scoped>
.ag-theme-alpine {
  --ag-secondary-border-color: none;
  --ag-font-size: 15px;
  --ag-foreground-color: rgb(57, 59, 51);
  --ag-background-color: rgb(231, 247, 255);
  --ag-header-foreground-color: rgb(57, 59, 51);
  --ag-header-background-color: rgb(198, 232, 255);
  --ag-odd-row-background-color: rgb(0, 0, 0, 0.03);
  --ag-header-column-resize-handle-color: rgb(74, 74, 224);
}
</style>
