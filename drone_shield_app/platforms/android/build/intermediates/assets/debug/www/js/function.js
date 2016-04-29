function getNfz(lat, lng){
        $.ajax
        ({
            type:'GET',
            url:'http://13.94.202.195/nfz',
            data:{'lat':lat, 'lng':lng},
            cache:true,
            success:function(html)
                {
                    window.localStorage.setItem('json-nfz', html);
                }
        });
    
}

function getObstacle(lat, lng){
        $.ajax
        ({
            type:'GET',
            url:'http://13.94.202.195/getobstacles',
            data:{'lat':lat, 'lng':lng},
            cache:true,
            success:function(html)
                {
                    window.localStorage.setItem('json-obs', html);
                }
        });
    
}



function drawCircle(level, city, radius, map){
    var colors = {};
    switch(level){
        case 0:
            colors[0] = "#0c559f";
            colors[1] = "#1f00dd";
            break;
        case 3:
            colors[0] = "#e9dd1b";
            colors[1] = "#928900";
            break;
        case 4:
            colors[0] = "#f32fff";
            colors[1] = "#57005c";
            break;
        default:
            colors[0] = "#cc0707";
            colors[1] = "#a50000";

    }

        var cityCircle = new google.maps.Circle({
            strokeColor: color[0],
            strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: color[1],
      fillOpacity: 0.35,
      map: map,
      center: city,
      radius: 500
    });
        return map;
}