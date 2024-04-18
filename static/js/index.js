"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


app.data = {    
    data: function() {
        return {
            sightings: [],
            new_species: "",
        };
    },
    methods: {
        // Complete as you see fit.
        add_sighting: function() {
            // This is time 1, the time of the button click.
            let self = this; 
            axios.post(add_sighting_url, {
                bird_species: this.new_species,
            }).then(function (r) {
                // This is time 2, much later, when the server answer comes back. 
                console.log("Got the id");
                self.sightings.push({
                    id: r.data.id,
                    bird_species: app.vue.new_species,
                    bird_count: 1,
                });
                self.new_species = "";
            });
            // This happens right after time 1, before time 2. 
            console.log("I am a happy coder"); 
        },
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    axios.get(load_sightings_url).then(function (r) {
        console.log(r.status);
        app.vue.sightings = r.data.sightings;
    });
}

app.load_data();

