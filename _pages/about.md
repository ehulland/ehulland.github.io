---
permalink: /
title: "About me"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

* Currently working as postdoc in the [Department of Viroscience at Erasmus MC](https://www.erasmusmc.nl/en/research/departments/viroscience), [GGD Rotterdam-Rijnmond](https://www.ggdrotterdamrijnmond.nl/), and the [Pandemic and Disaster Preparedness Center](https://convergence.nl/pandemic-disaster-preparedness-center/) working on the [Frontrunner 5 Project: Integrated early-warning surveillance methods and tools](https://convergence.nl/pandemic-disaster-preparedness-center/research/integrated-early-warning-surveillance-methods-and-tools/).

* Previously worked as a postdoctoral research consultant in the [Majumder Lab](https://lab.maimunamajumder.com/) at Boston Children's Hospital and Harvard Medical School, focusing on the role of trust (and mistrust) in society and on pandemic preparedness and response. 

* PhD graduate in [Global Health - Metrics Track](https://globalhealth.washington.edu/education-training/phd-gh) from the University of Washington, advised by [Dr. David Pigott](https://globalhealth.washington.edu/faculty/david-pigott) focusing on pandemic preparedness and the response to COVID-19. 

* Experience in international health, pandemic preparedness, and outbreak response with a strong interest in data science, statistics, and geospatial analyses.

* Research goals include improving pandemic preparedness modeling and response for diseases of epidemic potential. Experience in geospatial analysis, forecasting, survey design and analysis, and hierarchical modeling. Proficient in R, SAS, Git processes, some experience in Python. 

* Relevant coursework includes: Time series analysis, Maximum likelihood estimation Hierarchical modeling, Geospatial analysis.

* Extracurricular activities include spending time with my husband, daughter, newborn son, and two dogs exploring our new residence in Utrecht, Netherlands. 

* Full CV available upon request


<!-- ===================== -->
<!-- INTERACTIVE LEAFLET MAP -->
<!-- ===================== -->

<h2>Places I've Lived, Studied, and Worked</h2>
<p>
  This interactive map shows my trajectory over time.  
  Use the dropdown to zoom to a specific place.
</p>

<label for="placeSelect"><strong>Jump to place:</strong></label>
<select id="placeSelect">
  <option value="">– Select a place –</option>
</select>

<div id="placesMap" style="height: 500px; margin-top: 1rem;"></div>

<script>
  // 1. Your locations
  const places = [
    {
      name: "London, Canada",
      coords: [42.9849, -81.2453],
      role: "Lived"
    },
    {
      name: "Pittsburgh, PA, USA",
      coords: [40.4406, -79.9959],
      role: "Lived"
    },
    {
      name: "University Park, PA, USA",
      coords: [40.7982, -77.8599],
      role: "Studied (Bachelor's)"
    },
    {
      name: "Atlanta, GA, USA",
      coords: [33.7490, -84.3880],
      role: "Studied (MPH) and worked"
    },
    {
      name: "Seattle, WA, USA",
      coords: [47.6062, -122.3321],
      role: "Studied (PhD) and worked"
    },
    {
      name: "Utrecht, Netherlands",
      coords: [52.0907, 5.1214],
      role: "Lived and worked"
    }
  ];

  // 2. Initialize the map
  const map = L.map('placesMap');

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
  }).addTo(map);

  // 3. Add markers + popups + auto-fit bounds
  const bounds = L.latLngBounds();

  places.forEach(p => {
    const marker = L.marker(p.coords).addTo(map);
    marker.bindPopup(`<strong>${p.name}</strong><br>${p.role}`);
    bounds.extend(p.coords);
  });

  map.fitBounds(bounds.pad(0.2));

  // 4. Dropdown “fly-to” location selector
  const select = document.getElementById('placeSelect');

  places.forEach((p, idx) => {
    const opt = document.createElement('option');
    opt.value = idx;
    opt.textContent = p.name + " — " + p.role;
    select.appendChild(opt);
  });

  select.addEventListener('change', function () {
    if (this.value === "") return;
    const idx = parseInt(this.value, 10);
    const p = places[idx];
    map.flyTo(p.coords, 10, { duration: 1.5 });
  });
</script>

