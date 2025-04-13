# Rise-Well Alarm Clock

## 📚 Overview

This repository is split into two main folders:

- **`iot-alarm-clock`**: Contains Python scripts designed to run on the Raspberry Pi OS.
- **`webapp`**: Includes both the frontend and backend (server APIs) built using Next.js, TypeScript, TailwindCSS, and Shadcn.
- **`AI_sleep_detection`**: Contains python scripts for processing raw files and training the sleep detection model.
---

##  Setup & Running Instructions

### Running the IoT Alarm Clock (`iot-alarm-clock`)

1. SSH into your Raspberry Pi via VNC.
2. Transfer the entire `iot-alarm-clock` folder to the Raspberry Pi.
3. Create a virtual environment and source into the virtual environment.
4. Navigate into the folder:

```bash
cd iot-alarm-clock
```
5. Install the pip modules
```bash
pip3 install -r requirements.txt
```
6. Run the script:

```bash
sudo python3 main.py
```

**Note:** The project uses separate folders for different functionalities. Ensure you add scripts accordingly.

---

### Running the Web Application (`webapp`)

1. Navigate to the webapp folder:

```bash
cd webapp
```

2. Create and populate your `.env` file (see `.env` section).

3. Install dependencies:

---
### Running the Docker Application (currently on rabbitmq server)
1. Navigate to root folder
2. docker-compose up -d

```bash
npm install
```

4. Install and configure MongoDB:

- [Download MongoDB Compass](https://www.mongodb.com/products/compass)

5. Start the development server:

```bash
npm run dev
```

---

## APIs

API endpoints must be added in the `webapp/src/app/api` folder. API paths follow this structure:

```
localhost:3000/api/{folder}
```

2 Ways to testing out your endpoints
1. Postman
2. Call it thru your frontend

**Example: Calling an API (GET) from frontend using useEffect:**
```tsx
useEffect(() => {
  const fetchAlarms = async () => {
    try {
      const res = await fetch('/api/alarm-history', {
        credentials: 'include',
      });
      const data = await res.json();
      const alarms = data.alarms as AlarmHistoryDto[];
      if (!res.ok) {
        setError(data.message || 'Error fetching alarms');
      } else {
        setAlarms(alarms);
      }
    } catch (err) {
      console.error('Error fetching alarms:', err);
      setError('Error fetching alarms');
    } finally {
      setLoading(false);
    }
  };

  fetchAlarms();
}, []);
```

Ensure DTOs (schemas) are created for your APIs and imported into the frontend for type safety.

---

## Auth

Authentication is managed through **Clerk**:

- User data is stored securely in Clerk.
- Use provided Clerk API keys in your `.env` file.

Get current user details:

```typescript
import { currentUser } from '@clerk/nextjs/server';
const user = await currentUser();
```

---

## Database

MongoDB is utilized due to its strengths in handling time-series and unstructured IoT data. Ensure your MongoDB URI is correctly set in your `.env` file.

---

## OpenAI Integration

Current implementation uses OpenAI API to generate sentences for recitation practice based on difficulty and number of words. For extended functionality, extract common logic for reuse.

---

## Frontend Stack

- Next.js (React + TypeScript)
- TailwindCSS
- [Shadcn UI Components](https://ui.shadcn.com/)

> **Important:** Pls type everything & avoid using `any` if not i will find u ;p

---

## Environment Variables (`.env`)

Add your `.env` file in the `webapp` folder with the following:

```env
MONGODB_URI=mongodb://localhost:27017/rise-well
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_cGV0LXJlcHRpbGUtNjkuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=sk_test_GwodRVWSIKYQhDC4EoQXwvgNVLheNdmaDfraAnVz6E
OPENAI_API_KEY=<<INSERT YOUR OPENAI API KEY>>
```

---

## NOTE

- Maintain folder structure clearly: separate concerns (IoT scripts, frontend, backend).
- Type everything strictly (TypeScript DTOs/schema).
- Clearly separate reusable logic (API calls, OpenAI, auth handling).
- Regularly test API endpoints with Postman or frontend hooks.
- To get local ip address: `ipconfig getifaddr en0`