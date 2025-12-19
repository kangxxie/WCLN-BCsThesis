"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const python_shell_1 = require("python-shell");
const path_1 = __importDefault(require("path"));
const app = (0, express_1.default)();
const PORT = process.env.PORT || 3000;
// Middleware
app.use((0, cors_1.default)()); // Permette al frontend di chiamare il backend
app.use(express_1.default.json());
// Helper function to run Python scripts
const runPythonScript = async (scriptName, scriptArgs = []) => {
    const scriptPath = path_1.default.join(__dirname, '../python-scripts');
    console.log('Script path:', scriptPath);
    console.log('Running script:', scriptName);
    console.log('Full path:', path_1.default.join(scriptPath, scriptName));
    // args support
    let options = {
        scriptPath: scriptPath,
        pythonPath: 'python',
        args: []
    };
    if (Array.isArray(scriptArgs)) {
        options.args = scriptArgs;
    }
    console.log('Eseguo Python con args:', options.args);
    try {
        const result = await python_shell_1.PythonShell.run(scriptName, options);
        return { success: true, data: result };
    } catch (error) {
        console.error(`Error running ${scriptName}:`, error);
        console.error('Error details:', error.message);
        return { success: false, error: error };
    }
};
// API Routes
app.get('/api/doppler', async (req, res) => {
    const frame_index = req.query.frame_index ? String(req.query.frame_index) : '0';
    const args = [frame_index];
    console.log('[BACKEND] /api/doppler chiamato. Frame richiesto:', frame_index, 'Args:', args);
    try {
        console.log('[BACKEND] Avvio Python script: doppler.py con args:', args);
        const result = await runPythonScript('doppler.py', args);
        // console.log(result);
        if (result.success) {
            console.log('[BACKEND] Python script eseguito con successo.');
            const pythonOutput = result.data.join('');
            let dopplerData;
            try {
                dopplerData = JSON.parse(pythonOutput);
            } catch (e) {
                console.error('Errore parsing JSON output:', e);
                return res.status(500).json({ error: 'Errore parsing JSON output' });
            }
            res.json({
                "Range-Doppler Map": dopplerData["Range-Doppler Map"],
                "frame_index": frame_index,
                "total_frames": dopplerData["available_frames"]
            });
        } else {
            console.error('[BACKEND] Python script fallito:', result.error);
            res.status(500).json({ error: 'Failed to execute Python script' });
        }
    } catch (error) {
        console.error('[BACKEND] Errore processing doppler data:', error);
        res.status(500).json({ error: 'Server error' });
    }
});
app.get('/api/angle', async (req, res) => {
    const frame_index = req.query.frame_index ? String(req.query.frame_index) : '0';
    const args = [frame_index];
    console.log('[BACKEND] /api/angle chiamato. Frame richiesto:', frame_index, 'Args:', args);
    try {
        console.log('[BACKEND] Avvio Python script: angle.py con args:', args);
        const result = await runPythonScript('angle.py', args);
        if (result.success) {
            console.log('[BACKEND] Python script eseguito con successo.');
            const pythonOutput = result.data.join('');
            let angleData;
            try {
                angleData = JSON.parse(pythonOutput);
            } catch (e) {
                console.error('Errore parsing JSON output:', e);
                return res.status(500).json({ error: 'Errore parsing JSON output' });
            }
            res.json({
                "Angle-Range Map": angleData["Angle-Range Map"],
                "frame_index": frame_index,
                "total_frames": angleData["available_frames"]
            });
        } else {
            console.error('[BACKEND] Python script fallito:', result.error);
            res.status(500).json({ error: 'Failed to execute Python script' });
        }
    } catch (error) {
        console.error('[BACKEND] Errore processing angle data:', error);
        res.status(500).json({ error: 'Server error' });
    }
});
app.get('/api/targets', async (req, res) => {
    // Ricevi frame_index come query param, default 0
    const frame_index = req.query.frame_index ? String(req.query.frame_index) : '0';
    const args = [frame_index];
    try {
        const result = await runPythonScript('targets.py', args);
        console.log(result);
        if (result.success) {
            const pythonOutput = result.data.join('');
            let targetsData;
            try {
                targetsData = JSON.parse(pythonOutput);
            } catch (e) {
                console.error('Errore parsing JSON output:', e);
                return res.status(500).json({ error: 'Errore parsing JSON output' });
            }
            // targetsData: { frame_index, predicted_targets }
            res.json(targetsData);
            console.log('Python script executed successfully');
        }
        else {
            res.status(500).json({ error: 'Failed to execute Python script' });
        }
    }
    catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});
app.get('/api/chart-data', async (_req, res) => {
    console.log('Chart data endpoint called');
    try {
        console.log('Running Python script: chart-data.py');
        const result = await runPythonScript('chart-data.py');
        //console.log('Python script result:', result);
        if (result.success) {
            console.log('Python script executed successfully');
            // Parse the JSON output from Python script
            const pythonOutput = result.data.join('');
            //console.log('Python output:', pythonOutput);
            const chartData = JSON.parse(pythonOutput);
            //console.log('Parsed chart data:', chartData);
            res.json({
                hours: chartData.hours,
                targets: chartData.targets,
                total_detections: chartData.total_detections,
                peak_hour: chartData.peak_hour,
                avg_per_hour: chartData.avg_per_hour
            });
        }
        else {
            console.error('Python script failed:', result.error);
            res.status(500).json({ error: 'Failed to execute Python script' });
        }
    }
    catch (error) {
        console.error('Error processing chart data:', error);
        res.status(500).json({ error: 'Server error' });
    }
});
// Start server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
