import streamlit as st
import streamlit.components.v1 as components
import time as t

def radar_animation(unique_key=None):
    # radar animation
    components.html(
        f'''
        <canvas id="radarCanvas_{unique_key}" width="300" height="300" style="background: transparent;"></canvas>
        <div id="scanMessage_{unique_key}" style="color: #39ff14; font-family: Fira Mono, monospace; text-align: center; margin-top: 10px;"></div>
        <script>
        const canvas = document.getElementById('radarCanvas_{unique_key}');
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = 120;
        let angle = 0;
        let animationId;
        let isScanning = true;
        let frozenAngle = 0;
        
        // Initialize radar dots
        let radarDots = [];
        
        function addRandomDot() {{
            const dotAngle = Math.random() * 2 * Math.PI;
            const dotDistance = Math.random() * (radius - 10) + 10;
            radarDots.push({{
                x: centerX + dotDistance * Math.cos(dotAngle),
                y: centerY + dotDistance * Math.sin(dotAngle),
                life: 100,
                maxLife: 100
            }});
        }}
        
        // Add initial dots
        for (let i = 0; i < 8; i++) {{
            addRandomDot();
        }}
        
        function drawRadar() {{
            // Clear entire canvas first
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Create circular clipping path
            ctx.save();
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.clip();
            
            // Fill circular background with dark color
            ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.fill();
            
            // Draw radar background circles (range rings)
            ctx.strokeStyle = 'rgba(57, 255, 20, 0.3)';
            ctx.lineWidth = 1;
            for (let i = 1; i <= 4; i++) {{
                ctx.beginPath();
                ctx.arc(centerX, centerY, (radius / 4) * i, 0, 2 * Math.PI);
                ctx.stroke();
            }}
            
            // Draw crosshairs
            ctx.beginPath();
            ctx.moveTo(centerX - radius, centerY);
            ctx.lineTo(centerX + radius, centerY);
            ctx.moveTo(centerX, centerY - radius);
            ctx.lineTo(centerX, centerY + radius);
            ctx.stroke();
            
            // Restore context to draw outer circle without clipping
            ctx.restore();
            
            // Draw outer radar circle border
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.strokeStyle = '#39ff14';
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Re-apply clipping for sweep and dots
            ctx.save();
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.clip();
            
            if (isScanning) {{
                // Draw animated sweep
                const sweepLength = Math.PI / 6;
                const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
                gradient.addColorStop(0, 'rgba(57,255,20,0.4)');
                gradient.addColorStop(1, 'rgba(57,255,20,0)');
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, angle, angle + sweepLength);
                ctx.closePath();
                ctx.fillStyle = gradient;
                ctx.fill();
                
                // Draw sweep line
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(centerX + radius * Math.cos(angle), centerY + radius * Math.sin(angle));
                ctx.strokeStyle = '#39ff14';
                ctx.lineWidth = 2;
                ctx.stroke();
                
                angle += 0.03;
                if (angle > 2 * Math.PI) angle = 0;
            }} else {{
                // Draw static sweep at frozen position
                const sweepLength = Math.PI / 6;
                const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
                gradient.addColorStop(0, 'rgba(57,255,20,0.4)');
                gradient.addColorStop(1, 'rgba(57,255,20,0)');
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, frozenAngle, frozenAngle + sweepLength);
                ctx.closePath();
                ctx.fillStyle = gradient;
                ctx.fill();
                
                // Draw static sweep line
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(centerX + radius * Math.cos(frozenAngle), centerY + radius * Math.sin(frozenAngle));
                ctx.strokeStyle = '#39ff14';
                ctx.lineWidth = 2;
                ctx.stroke();
            }}
            
            // Draw and update radar dots
            for (let i = radarDots.length - 1; i >= 0; i--) {{
                const dot = radarDots[i];
                const alpha = dot.life / dot.maxLife;
                
                ctx.fillStyle = `rgba(57, 255, 20, ${{alpha}})`;
                ctx.beginPath();
                ctx.arc(dot.x, dot.y, 4, 0, 2 * Math.PI);
                ctx.fill();
                
                // Add a glow effect
                ctx.shadowColor = '#39ff14';
                ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.arc(dot.x, dot.y, 3, 0, 2 * Math.PI);
                ctx.fill();
                ctx.shadowBlur = 0;
                
                dot.life -= 0.5;
                if (dot.life <= 0) {{
                    radarDots.splice(i, 1);
                }}
            }}
            
            // Randomly add new dots
            if (Math.random() < 0.008) {{
                addRandomDot();
            }}
            
            // Restore context from clipping
            ctx.restore();
            
            animationId = requestAnimationFrame(drawRadar);
        }}
        
        // Start the animation
        drawRadar();
        
        // Stop animation after 5 seconds and show completion message
        setTimeout(() => {{
            frozenAngle = angle; // Capture current angle before stopping
            isScanning = false;
        }}, 5000);
        </script>
        ''',
        height=400,
    )
    t.sleep(5)
    st.success("Scan complete! Loading results...")