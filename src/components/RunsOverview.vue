<script>

import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles//ag-grid.css";
import "ag-grid-community/styles//ag-theme-alpine.css";

export default {
  name: "RunsOverview",
  props: ['selectedAlg'], // Environment receives from AlgOverview and sends it here
  emits: ["selectedRun"],
  components: {
    AgGridVue
  }, 

  // Watches for changes in value for selectedAlg prop
  watch: {
    selectedAlg: function(newVal, oldVal) { 

      // Fetch new runs
      this.runs = this.$store.getters.GET_RUNS

      // Refresh the grid 
      this.updateGrid()
      console.log("nr runs in db: ", this.runs.length)
      console.log("exiting method")
    }
  },

  beforeMount() {
    this.gridOptions = {};

    // Define grid headers
    this.columnDefs= [
        { headerName: "ID", field: "id"},
        { headerName: "Reward", field: "reward"},
        { headerName: "Energy Usage (kWh)", field: "energy"},  
        { headerName: "Emissions (kg CO2)", field: "co2" },  
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

  created() { 

    // Only one row can be selected at a time from grid
    this.rowSelection = 'single';
    this.currentEnv = this.$store.getters.GET_CURRENT_ENV
    this.runs = this.$store.getters.GET_RUNS  


    this.rowData = this.immutableStore

  },

  data() {
    return {
      gridOptions: null,
      gridColumnApi: null,
      gridApi: null, 
      columnApi: null,
      defaultColDef: null,
      runs: [], 
      columnDefs: [],
      immutableStore: [],
      rowData: null,
      rowSelection: null,
      currentEnv: "",
      currentAlg: "",
      errorLabel: "",
    };
  },

  methods: {
    async onSelectRun() { 
        const selectedRows = this.gridApi.getSelectedRows() 
        
        //document.querySelector('#selectedRows2').innerHTML = selectedRows.length === 1 ? selectedRows[0].id : ''

        // Fetch the run
        await this.$store.dispatch('getRun', {id: selectedRows[0].id})

        //document.getElementById("selectedRows2").style.visibility = "hidden"; 

        console.log("CURRENT RUN: ", this.$store.getters.GET_CURRENT_RUN)
        // Telling the parent of this component that an algorithm has been selected and that runs can be shown
        this.$emit("selectedRun", this.$store.getters.GET_CURRENT_RUN) 
    }, 

    updateGrid() {
      // Mutating existing rowdata
      this.gridApi.setRowData([])
      let newRowData = []
      for (let i = 0; i < this.runs.length; i++) {
        const element = this.runs[i]
        newRowData.push({ 
          id: element.run_id, 
          reward: element.reward, 
          energy: element.energy_consumed, 
          co2: element.CO2_emissions
        })
      }
    

      console.log("newRowData.size : ", newRowData.length)
      this.immutableStore = newRowData
      this.gridApi.setRowData(this.immutableStore)

      //this.gridApi.setRowData(newRowData);
    },

    onGridReady(params) {
      console.log("runs length: ", this.runs.length)
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;

      //this.gridApi.setRowData([])
      let newRowData = []
      params.api.setRowData(newRowData)

      const updateData = (data) => params.api.setRowData(data);
      
      // Retrieve the necessary data from runs and convert each run to a row
      for (let i = 0; i < this.runs.length; i++) {
        const element = this.runs[i]
        newRowData.push({ 
          id: element.run_id, 
          reward: element.reward, 
          energy: element.energy_consumed, 
          co2: element.CO2_emissions
        })
      }
      this.immutableStore = newRowData
      console.log("immutable store: ", this.immutableStore)      

      updateData(this.immutableStore)
    },
  }
}
</script>

<template>  
<div id="selectedRows2">
  <h2>Step 2: Select a run</h2>
  <ag-grid-vue 
  @grid-ready="onGridReady"
  @selection-changed="onSelectRun"
  style="width: 90vh; height: 50vh"
  class="ag-theme-alpine"
  :defaultColDef="defaultColDef"
  :rowSelection="rowSelection"
  :columnDefs="columnDefs"
  :rowData="rowData"
  :animateRows="true">
  >
  </ag-grid-vue>
</div>

</template>

<style scss scoped>
.ag-theme-alpine {
  --ag-border-color:rgb(57, 59, 51);

  --ag-secondary-border-color: none;
  --ag-font-size: 15px;
  --ag-foreground-color: rgb(57, 59, 51);
  --ag-background-color: rgb(248, 235, 253);
  --ag-header-foreground-color: rgb(57, 59, 51);
  --ag-header-background-color: rgb(233, 209, 253);
  --ag-odd-row-background-color: rgb(0, 0, 0, 0.03);
  --ag-header-column-resize-handle-color: rgb(74, 74, 224);
}
</style>
