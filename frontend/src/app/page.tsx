"use client";

import { useEffect, useState } from "react";
import { 
  Box, 
  Container, 
  Typography, 
  Card, 
  CardContent, 
  Button, 
  Chip, 
  Stack,
  Grid,
  CircularProgress
} from "@mui/material";
import DnsIcon from '@mui/icons-material/Dns';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import StorageIcon from '@mui/icons-material/Storage';
import DataObjectIcon from '@mui/icons-material/DataObject';
import SpeedIcon from '@mui/icons-material/Speed';
import HubIcon from '@mui/icons-material/Hub';
import AppsIcon from '@mui/icons-material/Apps';

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<string>("Checking...");
  
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/health");
        if (res.ok) {
          setBackendStatus("Online");
        } else {
          setBackendStatus("Offline");
        }
      } catch {
        setBackendStatus("Offline");
      }
    };

    checkBackend();
  }, []);

  const isOnline = backendStatus === "Online";

  const architectureNodes = [
    { title: "Next.js Frontend", desc: "React App Router with Server Components", icon: <AppsIcon color="primary" />, color: "#6366f1" },
    { title: "FastAPI Gateway", desc: "Async API orchestration layer", icon: <HubIcon sx={{ color: "#10b981" }} />, color: "#10b981" },
    { title: "PostgreSQL DB", desc: "Relational data (Users & Bookings)", icon: <StorageIcon sx={{ color: "#3b82f6" }} />, color: "#3b82f6" },
    { title: "MongoDB Cluster", desc: "Document storage (Posts & Comments)", icon: <DataObjectIcon sx={{ color: "#22c55e" }} />, color: "#22c55e" },
    { title: "Redis Cache", desc: "High-speed memory store & task queue", icon: <SpeedIcon sx={{ color: "#ef4444" }} />, color: "#ef4444" },
  ];

  return (
    <Box 
      sx={{ 
        minHeight: '100vh', 
        display: 'flex', 
        flexDirection: 'column', 
        justifyContent: 'center',
        position: 'relative',
        overflow: 'hidden',
        py: 10
      }}
    >
      {/* Subtle Background Elements */}
      <Box 
        sx={{ 
          position: 'absolute', 
          top: '20%', 
          left: '50%', 
          transform: 'translate(-50%, -50%)', 
          width: 800, 
          height: 800, 
          bgcolor: 'primary.main', 
          borderRadius: '50%', 
          filter: 'blur(160px)', 
          opacity: 0.1,
          zIndex: -1 
        }} 
      />

      <Container maxWidth="lg">
        <Stack spacing={8} alignItems="center" textAlign="center">
          
          <Box>
            <Typography variant="h1" component="h1" fontWeight={800} gutterBottom sx={{
              background: 'linear-gradient(180deg, #FFFFFF 0%, rgba(255, 255, 255, 0.4) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.02em',
              mb: 2,
              fontSize: { xs: '3rem', md: '5rem' }
            }}>
              Scale-Ready Architecture
            </Typography>
            <Typography variant="h5" color="text.secondary" fontWeight={300} sx={{ maxWidth: 700, mx: 'auto' }}>
              Built for enterprise deployment. Featuring Docker Compose orchestration, dual databases, and a containerized Next.js & FastAPI stack.
            </Typography>
          </Box>

          <Card sx={{ width: '100%', maxWidth: 400 }}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Stack direction="row" spacing={1} alignItems="center" color="text.secondary">
                  <DnsIcon fontSize="small" />
                  <Typography variant="overline" letterSpacing={1.5}>Backend Cluster</Typography>
                </Stack>
                <Chip 
                  label={backendStatus} 
                  icon={backendStatus === "Checking..." ? <CircularProgress size={16} /> : (isOnline ? <CheckCircleIcon /> : <ErrorIcon />)}
                  color={backendStatus === "Checking..." ? "default" : (isOnline ? "success" : "error")}
                  variant="outlined"
                  size="small"
                />
              </Stack>
            </CardContent>
          </Card>

          <Box sx={{ width: '100%' }}>
            <Grid container spacing={3} justifyContent="center">
              {architectureNodes.map((node, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Card sx={{ height: '100%', transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-4px)' } }}>
                    <CardContent sx={{ textAlign: 'left', p: 3 }}>
                      <Box sx={{ p: 1.5, borderRadius: 2, display: 'inline-flex', bgcolor: `${node.color}15`, mb: 2 }}>
                        {node.icon}
                      </Box>
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        {node.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {node.desc}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>

          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} pt={4}>
            <Button variant="contained" color="primary" size="large" disableElevation sx={{ px: 4, py: 1.5 }}>
              Deploy Cluster
            </Button>
            <Button variant="outlined" color="inherit" size="large" sx={{ px: 4, py: 1.5 }}>
              View Docker Compose
            </Button>
          </Stack>

        </Stack>
      </Container>
    </Box>
  );
}
