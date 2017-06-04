
  $(document).ready(function() {

    $.getJSON("/dashboard/userExerciseChart",function(data){

      let options = {
        fullWidth: true,
        height: "245px",
        chartPadding: {
          right: 20
        }
      };

      Chartist.Line('#exercisesMadeByUser', data, options);

    });

  });
