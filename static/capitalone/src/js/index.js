function load_charts() {
  google.charts.load("current", {packages:["corechart"]});
  google.charts.setOnLoadCallback(drawChart);
}
server_ip = "52.77.240.18:8081"
// server_ip = "0.0.0.0:8081"

data = {
  content: null
}

function drawChart() {
  var dataC = google.visualization.arrayToDataTable(data.content.pie_content);

  var options = {
    pieHole: 0.4,
    colors: ['#3F51B5','#E8700C','#8BC34A', '#f4b642', '#f44242'],
    backgroundColor: 'transparent',
    legend: {
      alignment: 'center'
    },
    tooltip: {
      text: 'percentage'
    }
  };

  var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
  chart.draw(dataC, options);
}


$(document).ready(function() {
  // $.getJSON('http://' + server_ip + '/app_events', function(data) {
    $('.x_panel_calendar').fullCalendar({
      // allow "more" link when too many events
      events: 'http://' + server_ip + '/app_events'
    });
  // })


  console.log(annyang);
  if (annyang) {

      console.log(annyang+"inside if");
   // Let's define our first command. First the text we expect, and then the function it should call
   var commands = {
     'Show me my budgets': function() {
       $('#budgetspage').trigger('click');
     },
     // 'show *': function() {
     //  console.log('hello htere')
     // },
     'show': function() {
      console.log('hello htere')
     },
     'show me': function() {
      console.log('hello htere.. showing me')
     }
     // ,
     // '*': function() {
     //  console.log('hello tere');
     // }
   };

   // Add our commands to annyang
   annyang.addCommands(commands);

   // Start listening. You can call this here, or attach this call to an event, button, etc.
   annyang.start();
  }
});

var map;
function initMap() {
  $.getJSON("http://" + server_ip + "/app_content?coords=true", function(d) {
    data.content = d;
    map = new google.maps.Map($('#world-map-gdp')[0], {
      zoom: 4,
      center: new google.maps.LatLng(40.459483,-91.0598467),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    setmarkers(d);
    updateBalanceDueCredit(d);
    addTransactionsToList($(".x_panel.transactions ul").last(), d.transactions, '');
    load_charts();
  });
}

function updateBalanceDueCredit(data) {
  $($(".row.tile_count .tile_stats_count .count").get(0)).html(data.curr_bal.val)
  $($(".row.tile_count .tile_stats_count .count").get(1)).html(data.curr_bal['text-sub'])
  $($(".row.tile_count .tile_stats_count .count").get(2)).html(data.credit.val)
  $($(".row.tile_count .tile_stats_count .count").get(3)).html(data.credit['text-sub'])
}

function addTransactionsToList(dom_object, transactions, additional_class) {
    var count = 0;
    $.each(transactions, function(index, transaction) {
      count += 1;
      $(dom_object).append('<li>' + 
          '<div class="name">' + transaction.name + '</div>' +
          '<div class="timestamp">' + transaction.date + '</div>' +
          '<div class="amount ' + (transaction.amount[0] == '-' ? 'negative' : '') + additional_class + '">' + transaction.amount + '</div>' +
          '</li>')
    });
}

function setmarkers(data) {
  data.transactions.forEach(function(d) {
   var marker = new google.maps.Marker({
       position:new google.maps.LatLng(d.lat, d.lon) ,
       map: map,
       title: d.name
     });
  });
}