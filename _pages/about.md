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

## Places I've Lived, Studied, and Worked

<p>
  Scroll through my journey below and watch the map follow along.
</p>

<div class="journey-layout">
  <!-- Map column -->
  <div class="journey-map-column">
    <div id="placesMap"></div>
  </div>

  <!-- Text / story column -->
  <div class="journey-text-column">
    <section class="journey-step" data-place-id="london-canada">
      <h3>London, Canada – Lived</h3>
      <p>
        This is where it started: living in London, Canada.
      </p>
    </section>

    <section class="journey-step" data-place-id="pittsburgh">
      <h3>Pittsburgh, PA, USA – Lived</h3>
      <p>
        A chapter spent living in Pittsburgh.
      </p>
    </section>

    <section class="journey-step" data-place-id="university-park">
      <h3>University Park, PA, USA – Bachelor's</h3>
      <p>
        Studied for my bachelor's degree at University Park.
      </p>
    </section>

    <section class="journey-step" data-place-id="atlanta">
      <h3>Atlanta, GA, USA – MPH & Work</h3>
      <p>
        Completed my MPH and worked in Atlanta.
      </p>
    </section>

    <section class="journey-step" data-place-id="seattle">
      <h3>Seattle, WA, USA – PhD & Work</h3>
      <p>
        PhD life (and work) in Seattle.
      </p>
    </section>

    <section class="journey-step" data-place-id="utrecht">
      <h3>Utrecht, Netherlands – Lived & Worked</h3>
      <p>
        Living and working in Utrecht.
      </p>
    </section>
  </div>
</div>

<script>
  // --- 1. Define your locations ---
  const places = {
    "london-canada": {
      name: "London, Canada",
      coords: [42.9849, -81.2453],
      role: "Lived"
    },
    "pittsburgh": {
      name: "Pittsburgh, PA, USA",
      coords: [40.4406, -79.9959],
      role: "Lived"
    },
    "university-park": {
      name: "University Park, PA, USA",
      coords: [40.7982, -77.8599],
      role: "Studied (Bachelor's)"
    },
    "atlanta": {
      name: "Atlanta, GA, USA",
      coords: [33.7490, -84.3880],
      role: "Studied (MPH), and worked"
    },
    "seattle": {
      name: "Seattle, WA, USA",
      coords: [47.6062, -122.3321],
      role: "Studied (PhD), and worked"
    },
    "utrecht": {
      name: "Utrecht, Netherlands",
      coords: [52.0907, 5.1214],
      role: "Lived and worked"
    }
  };

  // --- 2. Initialize map ---
  const map = L.map('placesMap');

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Add markers and compute bounds
  const bounds = L.latLngBounds();

  Object.values(places).forEach(p => {
    L.marker(p.coords)
      .addTo(map)
      .bindPopup(`<strong>${p.name}</strong><br>${p.role}`);
    bounds.extend(p.coords);
  });

  map.fitBounds(bounds.pad(0.3));

  // --- 3. Scroll-driven behavior with IntersectionObserver ---
  const steps = document.querySelectorAll('.journey-step');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const placeId = entry.target.dataset.placeId;
        const place = places[placeId];
        if (place) {
          // Highlight active step
          steps.forEach(s => s.classList.remove('journey-step--active'));
          entry.target.classList.add('journey-step--active');

          // Fly map to this location
          map.flyTo(place.coords, 6, { duration: 1.5 });
        }
      }
    });
  }, {
    root: null,
    threshold: 0.5
  });

  steps.forEach(step => observer.observe(step));
</script>
