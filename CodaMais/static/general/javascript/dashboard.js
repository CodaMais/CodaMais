
  $(document).ready(function() {

    $.getJSON("/dashboard/userExerciseChart",function(data){

      var options = {
          seriesBarDistance: 20,
          axisX: {
              showGrid: false
          },
          height: "245px"
      };

      Chartist.Bar('#exercisesMadeByUser', data, options);

    });

  });
