$(function () {
  $('#sixty').highcharts({
    chart: {
      type: 'column'
    },
    title: {
      text: 'Practice - Past Sixty Days'
    },
    xAxis: {
      type: 'datetime',
      crosshair: true,
      title: {
        text: 'Date'
      },
      min: Date.UTC({{sixty_days_ago.year}},{{sixty_days_ago.month}}-1,{{sixty_days_ago.day}}),
      max: Date.UTC({{today.year}},{{today.month}}-1,{{today.day}})
    },
    yAxis: {
      min: 0,
      max: 90,
      title: {
        text: 'Time (mins)'
      }
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
          '<td style="padding:0"><b>{point.y} mins</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      column: {
        pointPadding: 0.2,
        borderWidth: 0
      }
    },
    series: [{
      name: 'Practice',
      data: [
        {% for session in sixty_sessions %}
          [Date.UTC({{session.date.year}},{{session.date.month}}-1,{{session.date.day}}), {{session.minutes}}],
        {% endfor %}
      ]
    }]
  });
});
