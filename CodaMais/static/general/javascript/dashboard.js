

  $(document).ready(function() {

    var data = {
              labels: ['20/Jan - 30/Jan', '20/Feb - 20/Feb', '20/Mar - 20/Mar', '20/Abr - 20/Abr', '20/Mai - 20/Mai'],
              series: [
                [542, 443, 320, 600, 553],
                [412, 243, 280, 580, 453]
              ]
            };

            var options = {
                seriesBarDistance: 20,
                axisX: {
                    showGrid: false
                },
                height: "245px"
            };

            Chartist.Bar('#exercisesMadeByUser', data, options);
  });
