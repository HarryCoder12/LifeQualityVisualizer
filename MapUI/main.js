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
        center: ol.proj.fromLonLat([0, 0]), // Center the map (in lon/lat)
        zoom: 2 // Initial zoom level
    })
});

// Create a vector layer to hold GeoJSON data
var heatmapLayer = new ol.layer.Heatmap({
    source: new ol.source.Vector({
        url: 'everything.geojson', // Load GeoJSON file
        format: new ol.format.GeoJSON()
    }),
    blur: 15,   // Adjusts the smoothness of the heatmap
    radius: 8,  // Controls the size of individual heat points
    weight: function(feature) {
        // Use the "value" property in GeoJSON to determine intensity
        return feature.get('value') || 1; // Default weight is 1 if "value" is missing
    }
});
// Add the vector layer with GeoJSON to the map
map.addLayer(heatmapLayer);