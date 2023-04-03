<script>

import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles//ag-grid.css";
import "ag-grid-community/styles//ag-theme-alpine.css";
import { fromShortToFull } from "../utils/mapping.js";
import AlgCellRenderer from "./AlgCellRenderer.js";

export default {
  name: "AlgsOverview",
  emits: ["showRuns"], 
  components: {
    AgGridVue,
    AlgCellRenderer,
  },

  created() {
    // Only one row can be selected at a time from grid
    this.rowSelection = 'single';

    // Get currently selected env
    this.currentEnv = this.$store.GET_CURRENT_ENV,

    // Get algs
    this.algorithmList = this.$store.getters.GET_ALGS

    // Define grid headers
    this.columnDefs= [
      { headerName: "", field: "", cellRenderer: "AlgCellRenderer", minWidth:50, maxWidth: 100},
      { headerName: "Algorithm", field: "full", minWidth: 150 },
      { headerName: "Best reward", field: "reward",  maxWidth: 150 },  
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
        defaultColDef: null,
        gridApi: null, 
        columnApi: null,
        algorithmList: [], 
        columnDefs: [],
        rowData: [],
        rowSelection: null,
        currentEnv: "",
        errorLabel: "",
        showRuns: false // TODO should and can probably be removed 
    };
  },

  methods: {
    async onSelectAlgorithm() { 
      const selectedRows = this.gridApi.getSelectedRows() 

      document.querySelector('#selectedRows1').innerHTML = selectedRows.length === 1 ? selectedRows[0].full : ''

      // Telling the parent of this component that an algorithm has been selected and that runs can be shown
      this.showRuns = true  

      // Emit the selected algorithm
      this.$emit("showRuns", selectedRows[0].full)
    }, 

    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;

      const updateData = (data) => params.api.setRowData(data);

      // Retrieve the necessary row data from algs
      for (let i = 0; i < this.algorithmList.length; i++) {
        const element = this.algorithmList[i]
        this.rowData.push({ full: fromShortToFull(element.alg), reward: element.reward })
      }
      updateData(this.rowData)
    },
  }
}
</script>

<template>
<div class="algContainer" id="selectedRows1">
  <h3>Step 1: Select your algorithm</h3>
  <ag-grid-vue 
  @grid-ready="onGridReady"
  @selection-changed="onSelectAlgorithm"
  style="width: 500px; height: 300px"
  class="ag-theme-alpine"
  :rowSelection="rowSelection"
  :columnDefs="columnDefs"
  :defaultColDef="defaultColDef"
  :rowData="rowData">
  </ag-grid-vue>
  
</div>
</template>

<style scss scoped >

.ag-theme-alpine {
  --ag-secondary-border-color: none;
  --ag-font-size: 15px;
  --ag-foreground-color: rgb(57, 59, 51);
  --ag-background-color: rgb(249, 245, 227);
  --ag-header-foreground-color: rgb(57, 59, 51);
  --ag-header-background-color: rgb(252, 246, 129);
  --ag-odd-row-background-color: rgb(0, 0, 0, 0.03);
  --ag-header-column-resize-handle-color: rgb(74, 74, 224);
}

</style>

