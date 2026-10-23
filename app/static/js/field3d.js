/**
 * Procedural 3D Swaying Wheat Field Environment
 * Built with Three.js InstancedMesh for extreme mobile/low-end device efficiency.
 */

class WheatField3D {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas || typeof THREE === "undefined") {
      console.warn("Three.js or Canvas not ready");
      return;
    }

    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.instancedWheat = null;
    this.pollenParticles = null;
    this.clock = new THREE.Clock();

    // Field configuration
    this.stalkCount = window.innerWidth < 768 ? 1400 : 2800; // Auto-scale for mobile
    this.fieldWidth = 40;
    this.fieldDepth = 40;
    this.windIntensity = 1.0;
    this.windSpeed = 1.6;

    this.init();
  }

  init() {
    // 1. Scene & Depth Fog
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0c1610);
    this.scene.fog = new THREE.FogExp2(0x0c1610, 0.035);

    // 2. Camera Setup
    const aspect = window.innerWidth / window.innerHeight;
    this.camera = new THREE.PerspectiveCamera(50, aspect, 0.1, 120);
    this.camera.position.set(0, 3.2, 12);
    this.camera.lookAt(0, 1.8, 0);

    // 3. Renderer with hardware optimization
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: window.devicePixelRatio < 2,
      powerPreference: "high-performance",
      alpha: false
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.1;

    // 4. Lighting
    const ambientLight = new THREE.AmbientLight(0xffecc4, 0.7);
    this.scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xf59e0b, 1.6);
    sunLight.position.set(15, 20, 10);
    this.scene.add(sunLight);

    const skyFill = new THREE.HemisphereLight(0x38bdf8, 0x14532d, 0.6);
    this.scene.add(skyFill);

    // 5. Build Procedural Wheat & Pollen
    this.createWheatField();
    this.createPollenParticles();

    // 6. Window Resize & Parallax
    window.addEventListener("resize", () => this.onWindowResize());
    window.addEventListener("mousemove", (e) => this.onMouseMove(e));

    // 7. Start Render Loop
    this.animate();
  }

  createWheatField() {
    // Composite geometry: Thin flexible stem + tapered golden grain head
    const stemGeom = new THREE.CylinderGeometry(0.02, 0.035, 2.2, 5);
    stemGeom.translate(0, 1.1, 0); // Pivot at ground base

    const headGeom = new THREE.ConeGeometry(0.075, 0.8, 5);
    headGeom.translate(0, 2.4, 0); // Sits on top of stem

    // Combine into single efficient geometry
    const wheatGeom = new THREE.BufferGeometry();
    // InstancedMesh using a custom phong material with vertex colors
    const wheatMaterial = new THREE.MeshLambertMaterial({
      color: 0xfbbf24,
      emissive: 0x3d2b07,
      reflectivity: 0.2
    });

    this.instancedWheat = new THREE.InstancedMesh(stemGeom, wheatMaterial, this.stalkCount);
    this.dummy = new THREE.Object3D();
    this.stalkPositions = [];
    this.stalkRotations = [];

    const colorPalette = [
      new THREE.Color(0xd97706), // Golden Amber
      new THREE.Color(0xf59e0b), // Ripe Wheat
      new THREE.Color(0xfbbf24), // Sunlit Straw
      new THREE.Color(0x65a30d), // Young Green
      new THREE.Color(0x84cc16)  // Fresh Shoots
    ];

    for (let i = 0; i < this.stalkCount; i++) {
      // Distribute organically in a circular / elliptical spread
      const angle = Math.random() * Math.PI * 2;
      const radius = Math.sqrt(Math.random()) * (this.fieldWidth * 0.5);
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * (this.fieldDepth * 0.5) - 3;
      const y = (Math.sin(x * 0.1) + Math.cos(z * 0.1)) * 0.25;

      const scaleY = 0.85 + Math.random() * 0.45;
      const scaleXZ = 0.8 + Math.random() * 0.4;
      const initialTilt = (Math.random() - 0.5) * 0.15;

      this.dummy.position.set(x, y, z);
      this.dummy.scale.set(scaleXZ, scaleY, scaleXZ);
      this.dummy.rotation.set(initialTilt, Math.random() * Math.PI, initialTilt);
      this.dummy.updateMatrix();

      this.instancedWheat.setMatrixAt(i, this.dummy.matrix);

      // Assign realistic gradient tint
      const col = colorPalette[Math.floor(Math.random() * colorPalette.length)];
      this.instancedWheat.setColorAt(i, col);

      // Store base reference for wind computation
      this.stalkPositions.push({ x, y, z, scaleY, initialTilt, phase: Math.random() * Math.PI * 2 });
    }

    this.instancedWheat.instanceMatrix.needsUpdate = true;
    if (this.instancedWheat.instanceColor) this.instancedWheat.instanceColor.needsUpdate = true;
    this.scene.add(this.instancedWheat);
  }

  createPollenParticles() {
    const particleCount = 200;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 35;
      positions[i + 1] = Math.random() * 6;
      positions[i + 2] = (Math.random() - 0.5) * 35;
    }

    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
      color: 0xfef08a,
      size: 0.12,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending
    });

    this.pollenParticles = new THREE.Points(geometry, material);
    this.scene.add(this.pollenParticles);
  }

  onWindowResize() {
    if (!this.camera || !this.renderer) return;
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  onMouseMove(e) {
    const normX = (e.clientX / window.innerWidth - 0.5) * 2;
    const normY = (e.clientY / window.innerHeight - 0.5) * 2;

    if (this.camera) {
      this.camera.position.x += (normX * 1.5 - this.camera.position.x) * 0.05;
      this.camera.position.y += ((3.2 - normY * 0.8) - this.camera.position.y) * 0.05;
      this.camera.lookAt(0, 1.8, 0);
    }
  }

  setWindGust(isGusting) {
    this.windIntensity = isGusting ? 2.5 : 1.0;
    this.windSpeed = isGusting ? 3.2 : 1.6;
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    const delta = this.clock.getDelta();
    const elapsedTime = this.clock.getElapsedTime();

    // 1. Wind undulation physics across the crop field
    if (this.instancedWheat && this.stalkPositions) {
      const time = elapsedTime * this.windSpeed;

      // Update a batch of stalks per frame for maximum 60FPS smoothness
      for (let i = 0; i < this.stalkCount; i++) {
        const item = this.stalkPositions[i];

        // 2D Wave function propagating across field (X-Z diagonal wind)
        const wave1 = Math.sin(time + item.x * 0.25 + item.z * 0.15 + item.phase);
        const wave2 = Math.cos(time * 0.7 + item.x * 0.1 - item.z * 0.2);
        const bend = (wave1 * 0.7 + wave2 * 0.3) * 0.22 * this.windIntensity;

        this.dummy.position.set(item.x, item.y, item.z);
        this.dummy.scale.set(1, item.scaleY, 1);
        this.dummy.rotation.set(
          item.initialTilt + bend,
          bend * 0.5,
          item.initialTilt + bend * 0.6
        );
        this.dummy.updateMatrix();

        this.instancedWheat.setMatrixAt(i, this.dummy.matrix);
      }
      this.instancedWheat.instanceMatrix.needsUpdate = true;
    }

    // 2. Pollen particle drift
    if (this.pollenParticles) {
      const pos = this.pollenParticles.geometry.attributes.position.array;
      for (let i = 0; i < pos.length; i += 3) {
        pos[i] += 0.015 * this.windIntensity; // drift with wind
        pos[i + 1] += Math.sin(elapsedTime + pos[i]) * 0.003;
        if (pos[i] > 18) pos[i] = -18;
      }
      this.pollenParticles.geometry.attributes.position.needsUpdate = true;
    }

    this.renderer.render(this.scene, this.camera);
  }
}
