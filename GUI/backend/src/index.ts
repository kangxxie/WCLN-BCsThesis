import express, { Request, Response } from 'express';
import cors from 'cors';
import { PythonShell } from 'python-shell';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors()); // Permette al frontend di chiamare il backend
app.use(express.json());

// Helper function to run Python scripts
const runPythonScript = async (scriptName: string, args: string[] = []): Promise<any> => {
  const scriptPath = path.join(__dirname, '../python-scripts');
  console.log('Script path:', scriptPath);
  console.log('Running script:', scriptName);
  console.log('Full path:', path.join(scriptPath, scriptName));
  
  const options = {
    scriptPath: scriptPath,
    pythonPath: 'python',
    args: args
  };

  try {
    const result = await PythonShell.run(scriptName, options);
    console.log('Python script executed successfully, output:', result);
    return { success: true, data: result };
  } catch (error) {
    console.error(`Error running ${scriptName}:`, error);
    console.error('Error details:', (error as any).message);
    return { success: false, error: error };
  }
};

// API Routes
app.get('/api/doppler', async (req: Request, res: Response) => {
  //console.log('Doppler endpoint chiamato');
  try {
    // Forza max_frames=1 per simulazione live
    const frame_index = req.query.frame_index ? String(req.query.frame_index) : '0';
    const args = [frame_index];
    const result = await runPythonScript('doppler.py', args);
    if (result.success) {
      const pythonOutput = result.data.join('');
      let dopplerData;
      try {
        dopplerData = JSON.parse(pythonOutput);
      } catch (e) {
        console.error('Errore parsing JSON output:', e);
        return res.status(500).json({ error: 'Errore parsing JSON output' });
      }
      // Restituisci solo il frame richiesto (come array di 1 frame)
      res.json({
        "Range-Doppler Map": dopplerData["Range-Doppler Map"],
        "frame_index": frame_index,
        "total_frames": dopplerData["available_frames"]
      });
    } else {
      console.error('Python script failed:', result.error);
      res.status(500).json({ error: 'Failed to execute Python script' });
    }
  } catch (error) {
    console.error('Error processing doppler data:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

app.get('/api/angle', async (_req: Request, res: Response) => {
  try {
    const frame_index = _req.query.frame_index ? String(_req.query.frame_index) : '0';
    const args = [frame_index];
    const result = await runPythonScript('angle.py', args);
    if (result.success) {
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
      console.error('Python script failed:', result.error);
      res.status(500).json({ error: 'Failed to execute Python script' });
    }
  } catch (error) {
    console.error('Error processing angle data:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

app.get('/api/targets', async (req: Request, res: Response) => {
  // Ricevi frame_index come query param, default 0
  const frame_index = req.query.frame_index ? String(req.query.frame_index) : '0';
  const args = [frame_index];
  try {
    const result = await runPythonScript('targets.py', args);
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
    } else {
      res.status(500).json({ error: 'Failed to execute Python script' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

app.get('/api/chart-data', async (_req: Request, res: Response) => {
  //console.log('Chart data endpoint called');
  try {
    //console.log('Running Python script: chart-data.py');
    const result = await runPythonScript('chart-data.py');
    //console.log('Python script result:', result);

    if (result.success) {
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
    } else {
      console.error('Python script failed:', result.error);
      res.status(500).json({ error: 'Failed to execute Python script' });
    }
  } catch (error) {
    console.error('Error processing chart data:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
