geocoder = new google.maps.Geocoder();
totalMarkers = 0;

function initialize() 
{
    var mapOptions = {
        zoom: 15,
        disableDefaultUI: true,
        center: new google.maps.LatLng(30.627904, -96.334927),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);

    var input = document.getElementById('target');
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
    updateLocationName(name, position.nb, position.ob);

    if ('mk1' === name) {
        setCoordinateFrom(position.nb, position.ob);
    } else {
        setCoordinateTo(position.nb, position.ob);
    }

    var marker = new google.maps.Marker({
        draggable: true,
        position: position,
        map: map,
        name: name,
        icon: 'img/' + name + '.png',
        title: 'mk1' === name ? 'From Location' : 'To Location' 
    });
//            map.panTo(position);
    google.maps.event.addListener(marker, 'mouseup', function(e) {
        updateLocationName(name, e.latLng.nb, e.latLng.ob);

        if ('mk1' === name) {
            setCoordinateFrom(e.latLng.nb, e.latLng.ob);
        } else {
            setCoordinateTo(e.latLng.nb, e.latLng.ob);
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

function updateLocationName(name, latitude, longitude)
{
    locationName = 'Unknown';

        var latlng = new google.maps.LatLng(latitude, longitude);
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
            }/* else {
                alert("Geocoder failed due to: " + status);
            }*/
        });
}

$(document).ready(function() {
    google.maps.event.addDomListener(window, 'load', initialize);

    $('#start-time').timepicker();

    $('#route-form').submit(function() {
        $form = $(this);

        $.ajax({
            url: $form.attr('action'),
            type: 'post',
            data: $form.serialize(),
            success: function(data) {
                if (!data.error && typeof data.html !== 'undefined') {
                //     html = '';
                //     for (i in data.routes) {
                //         step = i + 1;
                //         html += '<tr><td>' + step + '</td>';
                //         html += '<td>' + data.routes[i].from + '</td>';
                //         html += '<td>' + data.routes[i].to + '</td>';
                //         html += '<td>' + data.routes[i].time + '</td>';
                //         html += '<td>' + data.routes[i].type + '</td>';
                //         html += '</tr>';
                //     }

                    $('#search-results').html(data.html);
                }
            },
            error: function(data) {
                console.log(data)
            }
        });
    })
});


        
        

        