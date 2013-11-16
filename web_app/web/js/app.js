var geocoder = new google.maps.Geocoder();
var totalMarkers = 0;
var busMarkers = [];
var map = null;

function initialize() 
{
    var mapOptions = {
        zoom: 15,
        disableDefaultUI: true,
        center: new google.maps.LatLng(30.627904, -96.334927),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
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
    updateLocationName(name, position.ob, position.pb);

    if ('mk1' === name) {
        setCoordinateFrom(position.ob, position.pb);
    } else {
        setCoordinateTo(position.ob, position.pb);
    }

    // create new marker
    var marker = new google.maps.Marker({
        draggable: true,
        position: position,
        map: map,
        name: name,
        icon: 'img/' + name + '.png',
        title: 'mk1' === name ? 'From Location' : 'To Location' 
    });
//            map.panTo(position);

    // bind action when moving marker
    google.maps.event.addListener(marker, 'mouseup', function(e) {
        updateLocationName(name, e.latLng.ob, e.latLng.pb);

        if ('mk1' === name) {
            setCoordinateFrom(e.latLng.ob, e.latLng.pb);
        } else {
            setCoordinateTo(e.latLng.ob, e.latLng.pb);
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

function addBusMarker(name, latitude, longitude)
{
    position = new google.maps.LatLng(latitude, longitude);

    var marker = new google.maps.Marker({
        position: position,
        map: map,
        name: name,
        icon: 'img/mk3.png',
        title: name
    });

    busMarkers.push(marker);
}

function addBusMarkers(markerData)
{
    for (i in markerData) {
        addBusMarker(markerData[i].name, markerData[i].latitude, markerData[i].longitude);
    }
}

function removeBusMarkers()
{
    for (var i = 0; i < busMarkers.length; i++) {
        busMarkers[i].setMap(null);
    }

    busMarkers = [];
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
                    $('#search-results').html(data.html);
                }
            },
            error: function(data) {
                console.log(data)
            }
        });
    });
});


        
        
