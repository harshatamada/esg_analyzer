// Dark/Light mode toggle
document.getElementById("mode-toggle").addEventListener("change", function () {
    document.body.classList.toggle("light-mode");
    document.body.classList.toggle("dark-mode");
    
    // Update toggle label
    const label = document.querySelector('label[for="mode-toggle"]');
    if (document.body.classList.contains('light-mode')) {
        label.textContent = '🌙 Dark Mode';
    } else {
        label.textContent = '☀️ Light Mode';
    }
});

// File input handling
document.getElementById('file-upload').addEventListener('change', function() {
    const label = document.getElementById('file-label');
    const fileName = this.files[0]?.name;
    
    if (fileName) {
        label.innerHTML = `📁 ${fileName}<br><small>File selected - ready to analyze!</small>`;
        label.classList.add('has-file');
    } else {
        label.innerHTML = '📄 Choose ESG Report File<br><small>PDF or TXT files only</small>';
        label.classList.remove('has-file');
    }
});

// Show info function
function showInfo(type) {
    const infoBox = document.getElementById("info-box");
    infoBox.style.display = "block";

    let content = "";

    switch (type) {
        case "project":
            content = `
                <h3>📋 About the Project</h3>
                <p>This ESG Risk Analyzer is a comprehensive tool designed to help organizations and investors evaluate environmental, social, and governance risks from corporate reports. Using advanced natural language processing techniques, it extracts key information from ESG reports and provides detailed risk assessments with actionable insights.</p>
                <p>The tool supports both PDF and text file formats, making it versatile for various types of ESG documentation.</p>
            `;
            break;
        case "esg":
            content = `
                <h3>🌱 About ESG & Its Uses</h3>
                <p>ESG (Environmental, Social, Governance) refers to the three key factors used to measure the sustainability and ethical impact of an investment in a company or business.</p>
                <p><strong>Environmental:</strong> Climate change, resource depletion, waste management, pollution<br>
                <strong>Social:</strong> Human rights, labor standards, community relations, diversity<br>
                <strong>Governance:</strong> Board composition, executive compensation, transparency, ethics</p>
                <p>ESG analysis helps investors make informed decisions while promoting sustainable business practices.</p>
            `;
            break;
        case "score":
            content = `
                <h3>📊 Risk Score Calculation</h3>
                <p>Our advanced risk scoring algorithm analyzes ESG reports through multiple steps:</p>
                <p>1. <strong>Text Extraction:</strong> Processes PDF and text documents to extract readable content<br>
                2. <strong>Keyword Identification:</strong> Identifies ESG-related terms and risk indicators<br>
                3. <strong>Severity Weighting:</strong> Assigns weights based on risk severity and frequency<br>
                4. <strong>Category Scoring:</strong> Calculates separate scores for Environmental, Social, and Governance factors<br>
                5. <strong>Overall Assessment:</strong> Provides a comprehensive risk score with detailed breakdown</p>
            `;
            break;
        case "custom":
            content = `
                <h3>⭐ Why ESG Matters</h3>
                <p>ESG analysis has become crucial for modern business and investment decisions:</p>
                <p><strong>Risk Management:</strong> Identifies potential legal, operational, and reputational risks before they impact business performance.</p>
                <p><strong>Investment Performance:</strong> Companies with strong ESG practices often demonstrate better long-term financial performance and resilience.</p>
                <p><strong>Regulatory Compliance:</strong> Helps organizations stay ahead of evolving environmental and social regulations.</p>
                <p><strong>Stakeholder Trust:</strong> Builds confidence among investors, customers, and communities through transparent sustainability practices.</p>
            `;
            break;
    }

    infoBox.innerHTML = content;
    
    // Smooth scroll to info box
    infoBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Add some interactive animations
document.addEventListener('DOMContentLoaded', function() {
    // Animate info box appearance
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    const infoBox = document.getElementById('info-box');
    infoBox.style.opacity = '0';
    infoBox.style.transform = 'translateY(20px)';
    infoBox.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(infoBox);
});