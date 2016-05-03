function set_weather (argument) {
    var xmlhttp, xmlDoc;
    xmlhttp     = new XMLHttpRequest();
    xmlhttp.open("GET", "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid=721943%20and%20u=%27c%27&format=xml&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys", false);
    xmlhttp.send();
    xmlDoc        = xmlhttp.responseXML;
    var weather   = xmlDoc.getElementsByTagName("condition")[0].getAttribute("text");
    var sunrise   = xmlDoc.getElementsByTagName("astronomy")[0].getAttribute("sunrise");
    var sunset    = xmlDoc.getElementsByTagName("astronomy")[0].getAttribute("sunset");
    var speed     = xmlDoc.getElementsByTagName("wind")[0].getAttribute("speed");
    var direction = xmlDoc.getElementsByTagName("wind")[0].getAttribute("direction");
    var temp      = xmlDoc.getElementsByTagName("condition")[0].getAttribute("temp");
    
    document.getElementById("response_weather").innerHTML = 'Fly Safe';
    document.getElementById("weather").innerHTML = weather;
    document.getElementById("sunrise").innerHTML = sunrise;
    document.getElementById("sunset").innerHTML = sunset;
    document.getElementById("speed").innerHTML = speed;
    document.getElementById("direction").innerHTML = direction+'°';
    document.getElementById("temp").innerHTML = temp+'°';
    document.getElementById("prob_rain").innerHTML = '50%';
    document.getElementById("geomagnetic").innerHTML = '4 Kp';


    date = xmlDoc.getElementsByTagName("forecast")[1].getAttribute("date");
    high = xmlDoc.getElementsByTagName("forecast")[1].getAttribute("high");
    text = xmlDoc.getElementsByTagName("forecast")[1].getAttribute("text");

    date_2 = xmlDoc.getElementsByTagName("forecast")[2].getAttribute("date");
    high_2 = xmlDoc.getElementsByTagName("forecast")[2].getAttribute("high");
    text_2 = xmlDoc.getElementsByTagName("forecast")[2].getAttribute("text");
}

function set_weather_next_day() {
    setTimeout(function(){   
        document.getElementById("date").innerHTML               = date;
        document.getElementById("high").innerHTML               = high+' C°';
        document.getElementById("weather_next_day").innerHTML   = text;
        document.getElementById("date_2").innerHTML             = date_2;
        document.getElementById("high_2").innerHTML             = high_2+' C°';
        document.getElementById("weather_next_day_2").innerHTML = text_2;
    }, 500);
}

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

function init(){
    StatusBar.backgroundColorByHexString("#15a3f4");

    function onConfirm(buttonIndex) {
        if (buttonIndex == 3 || buttonIndex == 0){
            navigator.app.exitApp()
        }
        if (buttonIndex == 1){
            startApp.set({"component": ["com.android.phone","com.android.phone.MobileNetworkSettings"]}).start();
        }
        if (buttonIndex == 2){
            startApp.set({"component": ["com.android.settings","com.android.settings.wifi.WifiSettings"]}).start();
        }
        
    }

   
        var networkState = navigator.connection.type;

        var states = {};
        states[Connection.UNKNOWN]  = 'Unknown connection';
        states[Connection.ETHERNET] = 'Ethernet connection';
        states[Connection.WIFI]     = 'WiFi connection';
        states[Connection.CELL_2G]  = 'Cell 2G connection';
        states[Connection.CELL_3G]  = 'Cell 3G connection';
        states[Connection.CELL_4G]  = 'Cell 4G connection';
        states[Connection.CELL]     = 'Cell generic connection';
        states[Connection.NONE]     = 'No network connection';

        if(states[networkState] == 'No network connection'){
            navigator.notification.confirm(
                'Switch on the internet connection',   
                onConfirm,              
                'No internet connection',      
                'Switch on 3G,Switch on Wifi,Exit'        
            ); 
        }
        else
        {
            set_weather();
        }      
}

function add_new_fly_zone (argument) {
    window.location ='#/add_new_fly_zone';
}

function view_maps(html) { 
    window.location ='#/view_maps';
    setTimeout(function(){

    window.onload = getNfz(42,12);
    // window.onload = getObstacle(42,12);
    var json = window.localStorage.getItem('json-nfz');
    //var json-obs = window.localStorage.getItem('json-obs');
    var arrays = JSON.parse(json);
    var defArrays = arrays.data;
            
    var directionsDisplay,
        directionsService,
        map;
    var colors = new Array("","");
    var level = 4;
            
       
    // Create marker
    var directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    var city = new google.maps.LatLng(42,12);
    var mapOptions = { zoom:12, mapTypeId: google.maps.MapTypeId.ROADMAP, center: city }
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
              
    for (var key in defArrays){
                   
        switch(defArrays[key].level){
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
                //alert(defArrays[key].name +" NAME - " + defArrays[key].lat +" lat - "+ defArrays[key].lng +" lng - ");
                  var radius = defArrays[key].radius;
                  if(radius < 100)
                      radius += 200;
                  //alert(defArrays[key].name);
                  city = new google.maps.LatLng(defArrays[key].lat,defArrays[key].lng);
                  var cityCircle = new google.maps.Circle({
                    strokeColor: colors[0],
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: colors[1],
                    fillOpacity: 0.35,
                    map: map,
                    center: city,
                    radius: radius
                  });
              }   
              var icon = "img/antenna.png";
              var beachMarker = new google.maps.Marker({
                position: {lat: 41.812345, lng: 12.512505},
                map: map,
                icon: icon
              });
              var icon = "img/drone.png";
              var beachMarker = new google.maps.Marker({
                position: {lat:  41.829079, lng: 12.464719},
                map: map,
                icon: icon
              });
              var icon = "img/pump.png";
              var beachMarker = new google.maps.Marker({
                position: {lat: 41.7875263, lng: 12.3581497},
                map: map,
                icon: icon
              });
              var icon = "img/drone.png";
              var beachMarker = new google.maps.Marker({
                position: {lat:  41.955961, lng: 12.464719},
                map: map,
                icon: icon
              }); 
              directionsDisplay.setMap(map);

              }, 500); 
        }