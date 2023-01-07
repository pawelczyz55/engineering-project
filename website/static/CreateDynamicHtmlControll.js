$(document).ready(function (){
    load();
});

function load(){
    //$("#txtQuantityCharts").focus();
    var quantity = 0;

    $("#btnQuantityCharts").click(function() {
        //$("#controllHtml").empty();
        //var QuantityCharts = $("#txtQuantityCharts").val();
        //alert(""+ QuantityCharts);

        //if(QuantityCharts > 0){
        //createControll(QuantityCharts);
        //}
        createControll(quantity);
        quantity += 1;
    });
}

//function createControll(QuantityCharts, quantity){
function createControll(quantity){
    var tbl = "";

    tbl = "<table>" +
        "<tr>" +
            "<th> S.No</th>" +
            "<th> First Name</th>"+
            "<th> Last Name</th>"+
            "<th> Gender</th>"+
            "<th> City</th>"+
        "</tr>";

    //for(i = 1; i <= QuantityCharts; i++){
    tbl += "<tr>" +
                "<td>" + quantity + "</td>" +

                "<td>"+
                    "<input type='text' id='txtFName' placeholder='First Name' autofocus />"+
                "</td>"+

                "<td>"+
                    "<input type='text' id='txtLName' placeholder='Last Name' />"+
                "</td>"+

                "<td>"+
                    "<input type='radio' name='Gender' value='M' /> Male <br />"+
                    "<input type='radio' name='Gender' value='F' /> Female"+
                "</td>"+

                "<td>"+
                    "<select id='ddlCity'>"+
                        "<option value='0'> - Select City - </option>"+
                        "<option value='1'> Porbandar </option>"+
                        "<option value='2'> Jamnagar </option>"+
                        "<option value='3'> Rajkot </option>"+
                        "<option value='4'> Baroda </option>"+
                        "<option value='5'> Mumbai </option>"+
                    "</select>"+
                "</td>" +
            "</tr>";
    //}
    tbl += "</table>"

    $("#controllHtml").append(tbl);
}