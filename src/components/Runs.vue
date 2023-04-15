<script>

import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles//ag-grid.css";
import "ag-grid-community/styles//ag-theme-alpine.css";

export default {
  name: "Runs",
  props: ["selectedAlg"], 
  emits: ["selectedRun"],
  components: {
    AgGridVue
  }, 

  watch: {
    /**
     * Watches for changes in value for selectedAlg prop
     * Value is handled in parent, but watch is needed still
     * for this class (child) to be made aware of the change
     */
    selectedAlg: function() { 

      // Fetch new runs 
      this.runs = this.$store.getters.GET_RUNS

      // Refresh the grid 
      this.updateGrid()
    }
  },

  beforeMount() {
    this.gridOptions = {};

    this.columnDefs= [
        { headerName: "ID", field: "id", maxWidth: 185, wrapText:true, autoHeight:true},
        { headerName: "Reward", field: "reward", maxWidth: 150, cellStyle: {textAlign: 'center'}, wrapText:true, autoHeight:true},
        { headerName: "Energy Usage (kWh)", field: "energy",  maxWidth: 180, cellStyle: {textAlign: 'center'}, wrapText:true, autoHeight:true},  
        { headerName: "Emissions (kg CO2)", field: "co2",  maxWidth: 170, cellStyle: {textAlign: 'center'}, wrapText:true, autoHeight:true },  
        { headerName: "Project name", field: "project_name", maxWidth: 170, cellStyle: {textAlign: 'left'}, wrapText:true, autoHeight:true },  
        { headerName: "Git link", field: "git_link", cellStyle: {textAlign: 'left'},wrapText:true, autoHeight:true },  

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
    this.rowSelection = 'single'
    this.domLayout = "autoHeight"
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
      domLayout: null,
      runs: [], 
      columnDefs: [],
      immutableStore: [],
      rowData: null,
      rowSelection: null,
      currentEnv: "",
      currentAlg: "",
    };
  },

  methods: {
    async onSelectRun() { 
        const selectedRows = this.gridApi.getSelectedRows() 
        
        // Fetch the run
        await this.$store.dispatch('getRun', {id: selectedRows[0].id})

        // Telling the parent of this component that an algorithm has been selected and that runs can be shown
        this.$emit("selectedRun", this.$store.getters.GET_CURRENT_RUN) 
    }, 

    /**
     * Updates grid upon prop-receival from parent. 
     * Updates when new algorithm is selected (Algs.vue)
     */
    updateGrid() {
      // Removing current row data
      this.gridApi.setRowData([])

      // RowData is immutable, thus we must create a new list
      let newRowData = []

      // Format row data from newly loaded runs
      for (let i = 0; i < this.runs.length; i++) {
        const element = this.runs[i]
        newRowData.push({ 
          id: element.run_id, 
          reward: element.reward, 
          energy: element.energy_consumed, 
          co2: element.CO2_emissions,
          project_name: element.project_name,
          git_link: element.git_link
        })
      }

      // Mutating mutable list "immutableStore" 
      this.immutableStore = newRowData
      this.gridApi.setRowData(this.immutableStore)
    },

    /**
     * Grid object is mounted to the DOM and rows are loaded into grid here
     * @param {*} params the current grid 
     */
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;

      let newRowData = []
      params.api.setRowData(newRowData)

      const updateData = (data) => params.api.setRowData(data);
      
      // Format data
      for (let i = 0; i < this.runs.length; i++) {
        const element = this.runs[i]
        newRowData.push({ 
          id: element.run_id, 
          reward: element.reward, 
          energy: element.energy_consumed, 
          co2: element.CO2_emissions,
          project_name: element.project_name,
          git_link: element.git_link
        })
      }

      // Add data to grid
      this.immutableStore = newRowData
      updateData(this.immutableStore)
    },
  }
}
</script>

<template>  
<div class="runs-container" id="selectedRows2">
  <h2>Step 2: Select a run</h2>
  <ag-grid-vue 
  @grid-ready="onGridReady"
  @selection-changed="onSelectRun"
  style="width: 130vh;"
  class="ag-theme-alpine"
  :defaultColDef="defaultColDef"
  :rowSelection="rowSelection"
  :columnDefs="columnDefs"
  :rowData="rowData"
  :domLayout="domLayout"
  :animateRows="true">
  >
  </ag-grid-vue>
</div>

</template>

<style lang="scss" scoped>
.ag-theme-alpine {
  --ag-border-color:rgb(57, 59, 51);

  --ag-secondary-border-color: none;
  --ag-font-size: 13px;
  --ag-foreground-color: rgb(57, 59, 51);
  --ag-background-color: rgb(248, 235, 253);
  --ag-header-foreground-color: rgb(57, 59, 51);
  --ag-header-background-color: rgb(233, 209, 253);
  --ag-odd-row-background-color: rgb(0, 0, 0, 0.03);
  --ag-header-column-resize-handle-color: rgb(74, 74, 224);
}
</style>
