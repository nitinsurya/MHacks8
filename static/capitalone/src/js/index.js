google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
var server_ip = '0.0.0.0:8081'
function drawChart() {
  console.log('hello there');
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

  var chart = new google.visualization.PieChart($('.x_panel_pie')[0]);
  chart.draw(data, options);
}

$(document).ready(function() {
		$('.x_panel_calendar').fullCalendar({
		// allow "more" link when too many events
			events: 'http://52.77.240.18:8081/app_events'
		});
});

var map;
function initMap(){
   map = new google.maps.Map($('#world-map-gdp')[0], {
    zoom: 10,
    center: new google.maps.LatLng(41.859483,-88.0598467),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  setmarkers();
}


function setmarkers() {
  $.getJSON("http://" + server_ip + "/app_content?coords=true",function(data){
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
 