// Create the map
var map = new ol.Map({
    target: 'map', // The div where the map will be placed
    layers: [
        // Add a base layer
        new ol.layer.Tile({
            source: new ol.source.OSM() // OpenStreetMap
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([14.47, 50.09  ]), // Center the map (in lon/lat)
        zoom: 16 // Initial zoom level
    })
});
let multiplicator = Array(0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5);
multiplicatorsum = 3.5;
function indexCalculator(data){

    var sum = 0;
    for(var i = 0; i<8; i++){
        sum+=data[i]*multiplicator[i];
    }
    return Math.tanh(sum/4000*2*3.5/multiplicatorsum);
}

// Create a vector layer to hold GeoJSON data
var heatmapLayer = new ol.layer.Heatmap({
    source: new ol.source.Vector({
        url: 'lifeQuality.geojson', // Load GeoJSON file
        format: new ol.format.GeoJSON()
    }),
    blur: 15,   // Adjusts the smoothness of the heatmap
    opacity: 0.7,
    radius: 15,  // Controls the size of individual heat points
    weight: function(feature) {
        // Use the "value" property in GeoJSON to determine intensity
        return indexCalculator(feature.values_.feature); // Default weight is 1 if "value" is missing
    }
});
// Add the vector layer with GeoJSON to the map
map.addLayer(heatmapLayer);
$("#navbutton").click(function(){
    $("#menu").toggle();
});
for (let i = 0; i <= 7; i++) {
    $(`#slider${i}`).on('input', function () {
        let val = $(this).val();
        $(`#sliderValue${i}`).text(val);
        multiplicator[i] = val/100;
    });
}
function newWeightFunction(feature) {
    // Use your new logic for weight calculation here
    return indexCalculator(feature.values_.feature);  // Assuming your GeoJSON has a 'newValue' field
}
$("#recountButton").click(function (){
    for(var j = 0; j<8; j++) {
        multiplicatorsum += multiplicator[j];
    }
    map.removeLayer(heatmapLayer);
    heatmapLayer = new ol.layer.Heatmap({
        source: new ol.source.Vector({
            url: 'lifeQuality.geojson', // Load GeoJSON file
            format: new ol.format.GeoJSON()
        }),
        blur: 15,   // Adjusts the smoothness of the heatmap
        opacity: 0.7,
        radius: 15,  // Controls the size of individual heat points
        weight: function(feature) {
            // Use the "value" property in GeoJSON to determine intensity
            return indexCalculator(feature.values_.feature); // Default weight is 1 if "value" is missing
        }
    });
    map.addLayer(heatmapLayer);
})
