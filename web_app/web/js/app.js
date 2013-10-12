function initialize() 
{
    geocoder = new google.maps.Geocoder();
    var mapOptions = {
        zoom: 4,
        center: new google.maps.LatLng(-25.363882,131.044922),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);

    var input = document.getElementById('from-location');
    var searchBox = new google.maps.places.SearchBox(input);

    google.maps.event.addListener(map, 'click', function(e) {
        if (totalMarkers >= 2) {
            return;
        }

        totalMarkers++;

        markerName = totalMarkers == 1 ? 'mk1' : 'mk2';
        
        placeMarker(markerName, e.latLng, map);
    });

    google.maps.event.addListener(searchBox, 'places_changed', function() {
        var places = searchBox.getPlaces();

        // For each place, get the icon, place name, and location.
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places[i]; i++) {
            var image = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            bounds.extend(place.geometry.location);
        }

        map.fitBounds(bounds);
    });
}

function placeMarker(name, position, map) 
{
    geocoder = new google.maps.Geocoder();

    if ('mk1' === name) {
        setCoordinateFrom(position.lb, position.mb);
    } else {
        setCoordinateTo(position.lb, position.mb);
    }

    var marker = new google.maps.Marker({
        draggable: true,
        position: position,
        map: map,
        name: name
    });
//            map.panTo(position);
    google.maps.event.addListener(marker, 'mouseup', function(e) {
        locationName = 'Unknown';

        var latlng = new google.maps.LatLng(e.latLng.lb, e.latLng.mb);
        geocoder.geocode({'latLng': latlng}, function(results, status, locationName) {
            if (status == google.maps.GeocoderStatus.OK) {
                locationName = '';

                for (index in results[0].address_components) {
                    locationName += results[0].address_components[index].long_name + ', ';
                }
                locationName = $.trim(locationName, ',');
                
                if ('mk1' === name) {
                    setLocationFrom(locationName);
                } else {
                    setLocationTo(locationName);
                }
            } else {
                alert("Geocoder failed due to: " + status);
            }
        });

        if ('mk1' === name) {
            setCoordinateFrom(e.latLng.lb, e.latLng.mb);
        } else {
            setCoordinateTo(e.latLng.lb, e.latLng.mb);
        }

        
    });
}

function setCoordinateFrom(latitude, longitude)
{
    $('#from-coordinate-lat').val(latitude);
    $('#from-coordinate-long').val(longitude);
}

function setCoordinateTo(latitude, longitude)
{
    $('#to-coordinate-lat').val(latitude);
    $('#to-coordinate-long').val(longitude);
}

function setLocationFrom(locationName)
{
    $('#from-location').val(locationName);
}

function setLocationTo(locationName)
{
    $('#to-location').val(locationName);
}

$(document).ready(function() {
    totalMarkers = 0;
    google.maps.event.addDomListener(window, 'load', initialize);

    $(' #timepicker1').timepicker();
});


        
        

        