$(document).ready(function (){
    load();
});

function load(){
    $("#txtQuantityCharts").focus();

    $("#btnQuantityCharts").click(function() {
        var QuantityCharts = $("#txtQuantityCharts").val();
        alert(""+ QuantityCharts);

        if(QuantityCharts > 0){
            createControll(QuantityCharts);
        }
    });
}

function createControll(QuantityCharts){
    
}