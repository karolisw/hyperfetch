<script>
import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles//ag-grid.css";
import "ag-grid-community/styles//ag-theme-alpine.css";

import { fromShortToFull } from "../utils/mapping.js";
import AlgCellRenderer from "./renderers/AlgCellRenderer.js";

export default {
  name: "Algs",
  emits: ["showRuns"], 
  components: {
    AgGridVue,
    AlgCellRenderer,
  },

  created() {
    // Only one row can be selected at a time 
    this.rowSelection = 'single';

    // Get currently selected env
    this.currentEnv = this.$store.GET_CURRENT_ENV,

    // Get algs for selected env
    this.algorithmList = this.$store.getters.GET_ALGS

    // Define grid headers
    this.columnDefs= [
      { headerName: "", field: "", cellRenderer: "AlgCellRenderer", minWidth:50, maxWidth: 100},
      { headerName: "Algorithm", field: "full", minWidth: 150 },
      { headerName: "Best reward", field: "reward",  maxWidth: 150 },  
    ]

    // Define grid structure
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
    };
  },

  methods: {

    /**
     * Event handler for user-click on single row in grid
     */
    async onSelectAlgorithm() { 
      const selectedRows = this.gridApi.getSelectedRows() 

      // Emit the selected algorithm to parent (Overview.vue)
      this.$emit("showRuns", selectedRows[0].full)
    }, 

    
    /**
     * Grid object is mounted to the DOM and rows are loaded into grid here
     * @param {*} params the current grid 
     */
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;

      const updateData = (data) => params.api.setRowData(data);

      // Reformate the data from algortithmList
      for (let i = 0; i < this.algorithmList.length; i++) {
        const element = this.algorithmList[i]
        this.rowData.push({ full: fromShortToFull(element.alg), reward: element.reward })
      }

      // Push data into grid
      updateData(this.rowData)
    },
  }
}
</script>

<template>
<div class="algContainer" id="selectedRows1">
  <h2>Step 1: Select your algorithm</h2>
  <ag-grid-vue 
  @grid-ready="onGridReady"
  @selection-changed="onSelectAlgorithm"
  style="width: 90vh; height: 35vh;"
  class="ag-theme-alpine"
  :rowSelection="rowSelection"
  :columnDefs="columnDefs"
  :defaultColDef="defaultColDef"
  :rowData="rowData"
>
  </ag-grid-vue>
  
</div>
</template>

<style lang="scss" scoped >

.ag-theme-alpine {
  --ag-border-color:rgb(57, 59, 51);
  --ag-secondary-border-color: none;
  --ag-font-size: 15px;
  --ag-foreground-color: rgb(57, 59, 51);
  --ag-background-color: rgb(235, 255, 212);
  --ag-header-foreground-color: rgb(57, 59, 51);
  --ag-header-background-color: rgb(217, 253, 160);
  --ag-odd-row-background-color: rgb(0, 0, 0, 0.03);
  --ag-header-column-resize-handle-color: rgb(74, 74, 224);
}
</style>

