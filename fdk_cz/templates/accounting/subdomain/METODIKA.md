# METODIKA: Zážitkové účetnictví
## Subdoména ucetnictvi.fdk.cz

---

## 1. KONCEPT

**"Zážitkové účetnictví"** = manažer má pocit, že řídí Airbus A380, i když jen schvaluje faktury! 🛫

### Hlavní pilíře:
- 🎨 **Vizuální extravagance** - každá akce je událost
- 💎 **Prémiový pocit** - jako v kokpitu letadla
- 🚀 **Interaktivita** - animace, přechody, efekty
- 📊 **Datová vizualizace** - grafy, gauges, indikátory
- 🎯 **Gamifikace** - progress bary, achievement badges
- 🔔 **Live notifikace** - real-time updates
- 🌈 **Gradient design** - moderní, žhavé barvy

---

## 2. DESIGNOVÁ FILOZOFIE

### Barvy & Gradienty
```
Primary Gradient:   linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Success Gradient:   linear-gradient(135deg, #11998e 0%, #38ef7d 100%)
Warning Gradient:   linear-gradient(135deg, #f093fb 0%, #f5576c 100%)
Info Gradient:      linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)
Dark Gradient:      linear-gradient(135deg, #2c3e50 0%, #34495e 100%)
```

### Typography
- **Headings**: Inter Bold / Poppins Bold
- **Body**: Inter Regular / System UI
- **Numbers**: JetBrains Mono / SF Mono (monospace)
- **Sizes**: Velké, výrazné nadpisy (2xl-4xl)

### Spacing
- Vzdušné rozestupy (min 1.5rem mezi sekcemi)
- Velké paddingy v kartách (p-6 až p-8)
- Bílý prostor je důležitý

### Shadows & Effects
```css
card-shadow: 0 4px 20px rgba(0,0,0,0.08)
hover-shadow: 0 8px 30px rgba(0,0,0,0.12)
glow-effect: 0 0 20px rgba(102,126,234,0.4)
```

---

## 3. KOMPONENTY

### 3.1 Dashboard Cards
- Velké KPI karty s gradientem
- Animované čísla (countup efekt)
- Ikonky 3-4em velikosti
- Sparkline grafy v pozadí

### 3.2 Data Tables
- Hover efekty s smooth transitions
- Alternating row colors (zebra striping)
- Sticky headers při scrollu
- Action buttons v dropdown menu

### 3.3 Forms
- Floating labels
- Icon prefixes
- Inline validace s animací
- Progress indicator pro multi-step forms

### 3.4 Charts & Graphs
- Chart.js nebo ApexCharts
- Animované načítání
- Interactive tooltips
- Responsive breakpoints

### 3.5 Navigation
- Sticky header s glassmorphism
- Breadcrumbs s animacemi
- Quick actions floating button (FAB)
- Sidebar collapse/expand

---

## 4. STRUKTURA ŠABLON

```
accounting/subdomain/
├── METODIKA.md                    # tento soubor
├── base.html                      # base s gradientem & efekty
├── components/
│   ├── kpi_card.html             # reusable KPI karta
│   ├── chart_wrapper.html        # wrapper pro grafy
│   ├── data_table.html           # stylizovaná tabulka
│   └── action_button.html        # CTA tlačítka
├── accounting_dashboard.html     # hlavní dashboard
├── balance_sheet.html            # rozvaha s vizualizací
├── journal_ledger.html           # deník s filtry
├── chart_of_accounts.html        # účtová osnova
├── list_invoices.html            # seznam faktur
├── create_invoice.html           # nová faktura
├── detail_invoice.html           # detail faktury
└── accounting_context.html       # výběr kontextu

```

---

## 5. UNIKÁTNÍ FEATURY

### 5.1 Cockpit Dashboard
- **Altitude**: Celkové výnosy (čím výš, tím líp)
- **Speed**: Rychlost inkasa faktur
- **Fuel**: Likvidita / cash flow
- **Engine Status**: Stav jednotlivých oblastí (faktury, deník, rozvaha)

### 5.2 Achievement System
- 🏆 **First Blood**: První faktura vystavena
- 💰 **Million Maker**: Celkové výnosy > 1M
- 📊 **Balanced**: 100% vyrovnaná rozvaha
- ⚡ **Flash**: Faktura zaplacena do 24h
- 🎯 **Sniper**: 0% po splatnosti

### 5.3 Real-Time Indicators
- Live dashboard s WebSocket updates
- Notifikace o změnách
- Auto-refresh KPI každých 30s

### 5.4 Data Export Premium
- PDF s branded designem
- Excel s formátováním
- CSV pro import do jiných systémů
- API endpoint pro integraci

---

## 6. ANIMACE & TRANSITIONS

```css
/* Smooth transitions všude */
* { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }

/* Card hover effect */
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

/* Button ripple effect */
.btn { position: relative; overflow: hidden; }
.btn::after { /* ripple animation */ }

/* Number countup */
@keyframes countup {
  from { opacity: 0; transform: scale(0.5); }
  to { opacity: 1; transform: scale(1); }
}
```

---

## 7. RESPONSIVITA

### Breakpoints
- **Mobile**: < 640px (stack everything)
- **Tablet**: 640px - 1024px (2 columns)
- **Desktop**: > 1024px (3-4 columns)
- **XL**: > 1280px (full dashboard layout)

### Mobile First
- Touch-friendly (min 44px touch targets)
- Swipe gestures
- Bottom navigation bar
- Pull to refresh

---

## 8. PERFORMANCE

### Optimalizace
- Lazy load images & charts
- Virtualized long lists
- Debounced search inputs
- Prefetch critical data
- Service worker pro offline

### Bundle Size
- Tailwind JIT (only used classes)
- Tree-shaking unused JS
- Compress images (WebP)
- Minify CSS/JS in production

---

## 9. ACCESSIBILITY

- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- High contrast mode
- Focus indicators
- Alt texts na všech obrázcích

---

## 10. DEMO MODE

Pro nepřihlášené uživatele:
- Předpřipravená demo data
- Realistické částky a názvy
- "DEMO" watermark
- CTA na registraci
- Limit funkcí (view only)

---

## 11. BEZPEČNOST

- CSRF protection všude
- SQL injection prevention (ORM)
- XSS protection (escape outputs)
- Rate limiting na API
- Secure session handling
- HTTPS only

---

## 12. FUTURE ROADMAP

### Fáze 1 (aktuální)
- ✅ Base design system
- ✅ Dashboard s KPI
- ✅ Faktury, deník, rozvaha

### Fáze 2 (Q1 2025)
- 📊 Advanced charts (ApexCharts)
- 🎮 Achievement system
- 📱 Mobile app (PWA)

### Fáze 3 (Q2 2025)
- 🤖 AI asistent pro účetnictví
- 📈 Prediktivní analýza
- 🔗 API pro třetí strany

---

**MOTTO**: "Každá faktura je událost. Každý zápis je mise. Každý report je triumf."

🚀 **Let's make accounting sexy again!**
