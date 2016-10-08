google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
var data = google.visualization.arrayToDataTable([
  ['category', 'amount'],
  ['Food', 4],
  ['Travel', 2],
  ['Entertainment', 2]
]);

var options = {
  title: 'Spend Summary',
  pieHole: 0.4,
  colors: ['#009688','#ff5722','#9c27b0']
};

var chart = new google.visualization.PieChart($.('x_panel_pie'));
chart.draw(data, options);
}

$(document).ready(function() {

		$.('x_panel_calender').fullCalendar({
		// allow "more" link when too many events
			events: './events.json'
		});
});

var map;
function initMap(){
 map = new google.maps.Map($.('x_panel_map')), {
  zoom: 10,
  center: new google.maps.LatLng(41.859483,-88.0598467),
  mapTypeId: google.maps.MapTypeId.ROADMAP

});
setmarkers();
}
function setmarkers()
{
  $.getJSON("http://52.77.240.18:8081/app_content?coords=true",function(data){
    console.log(data);
     data.transactions.forEach(function(d) {
       console.log(d);
       var marker = new google.maps.Marker({
           position:new google.maps.LatLng(d.lat, d.lon) ,
           map: map,
           title: d.name
         });
      });
    });
}
 