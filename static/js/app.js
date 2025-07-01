// Time & Attendance System JavaScript

// Global variables
let currentTime = new Date();
let clockInterval;

// Initialize the application
document.addEventListener("DOMContentLoaded", function () {
  initializeClock();
  initializeNotifications();
  initializeFormValidation();
  initializeModals();
});

// Clock functionality
function initializeClock() {
  const clockElement = document.getElementById("live-clock");
  if (clockElement) {
    clockInterval = setInterval(updateClock, 1000);
    updateClock();
  }
}

function updateClock() {
  const now = new Date();

  // Get IST time
  const timeString = now.toLocaleTimeString("en-IN", {
    hour12: true,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    timeZone: "Asia/Kolkata",
  });

  const dateString = now.toLocaleDateString("en-IN", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "Asia/Kolkata",
  });

  // Update main clock element if it exists
  const clockElement = document.getElementById("live-clock");
  if (clockElement) {
    clockElement.innerHTML = `
            <div class="text-lg font-bold text-primary-600">${timeString}</div>
            <div class="text-sm text-gray-600">${dateString}</div>
        `;
  }

  // Update navigation clock elements if they exist
  const timeElement = document.getElementById("current-time");
  const dateElement = document.getElementById("current-date");

  if (timeElement) {
    timeElement.textContent = timeString;
  }
  if (dateElement) {
    const shortDateString = now.toLocaleDateString("en-IN", {
      weekday: "short",
      day: "numeric",
      month: "short",
      timeZone: "Asia/Kolkata",
    });
    dateElement.textContent = shortDateString;
  }
}

// Notification system
function initializeNotifications() {
  // Check for browser notification support
  if ("Notification" in window) {
    if (Notification.permission === "default") {
      Notification.requestPermission();
    }
  }
}

function showNotification(title, message, type = "info") {
  // Browser notification
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification(title, {
      body: message,
      icon: "/static/images/icon.png",
    });
  }

  // In-app notification
  showAlert(message, type);
}

function showAlert(message, type = "info") {
  const alertContainer = document.createElement("div");
  alertContainer.className = `alert-floating alert alert-${type} bg-${getAlertColor(
    type
  )}-100 border border-${getAlertColor(type)}-400 text-${getAlertColor(
    type
  )}-700 px-4 py-3 rounded relative`;
  alertContainer.innerHTML = `
        <span class="block sm:inline">${message}</span>
        <span class="absolute top-0 bottom-0 right-0 px-4 py-3 cursor-pointer" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </span>
    `;

  document.body.appendChild(alertContainer);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (alertContainer.parentNode) {
      alertContainer.remove();
    }
  }, 5000);
}

function getAlertColor(type) {
  const colors = {
    success: "green",
    error: "red",
    warning: "yellow",
    info: "blue",
  };
  return colors[type] || "blue";
}

// Form validation
function initializeFormValidation() {
  const forms = document.querySelectorAll("form[data-validate]");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      if (!validateForm(this)) {
        e.preventDefault();
      }
    });
  });
}

function validateForm(form) {
  let isValid = true;
  const requiredFields = form.querySelectorAll("[required]");

  requiredFields.forEach((field) => {
    if (!field.value.trim()) {
      showFieldError(field, "This field is required");
      isValid = false;
    } else {
      clearFieldError(field);
    }
  });

  // Email validation
  const emailFields = form.querySelectorAll('input[type="email"]');
  emailFields.forEach((field) => {
    if (field.value && !isValidEmail(field.value)) {
      showFieldError(field, "Please enter a valid email address");
      isValid = false;
    }
  });

  // Password confirmation
  const passwordField = form.querySelector('input[name="password"]');
  const confirmPasswordField = form.querySelector(
    'input[name="confirm_password"]'
  );
  if (passwordField && confirmPasswordField) {
    if (passwordField.value !== confirmPasswordField.value) {
      showFieldError(confirmPasswordField, "Passwords do not match");
      isValid = false;
    }
  }

  return isValid;
}

function showFieldError(field, message) {
  clearFieldError(field);

  const errorElement = document.createElement("div");
  errorElement.className = "text-red-600 text-sm mt-1";
  errorElement.textContent = message;
  errorElement.id = `error-${field.name}`;

  field.parentNode.appendChild(errorElement);
  field.classList.add("border-red-500");
}

function clearFieldError(field) {
  const existingError = document.getElementById(`error-${field.name}`);
  if (existingError) {
    existingError.remove();
  }
  field.classList.remove("border-red-500");
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Modal functionality
function initializeModals() {
  const modalTriggers = document.querySelectorAll("[data-modal-target]");
  modalTriggers.forEach((trigger) => {
    trigger.addEventListener("click", function (e) {
      e.preventDefault();
      const targetModal = document.getElementById(this.dataset.modalTarget);
      if (targetModal) {
        showModal(targetModal);
      }
    });
  });

  const modalClosers = document.querySelectorAll("[data-modal-close]");
  modalClosers.forEach((closer) => {
    closer.addEventListener("click", function () {
      const modal = this.closest(".modal");
      if (modal) {
        hideModal(modal);
      }
    });
  });
}

function showModal(modal) {
  modal.classList.remove("hidden");
  modal.classList.add("flex");
  document.body.style.overflow = "hidden";
}

function hideModal(modal) {
  modal.classList.add("hidden");
  modal.classList.remove("flex");
  document.body.style.overflow = "";
}

// Attendance functions
function performCheckIn() {
  showLoading("Checking in...");

  return fetch("/attendance/check-in/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCsrfToken(),
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      hideLoading();
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        showNotification("Check-in Successful", data.message, "success");
        location.reload();
      } else {
        showNotification("Check-in Failed", data.error, "error");
      }
    })
    .catch((error) => {
      hideLoading();
      console.error("Error:", error);
      showNotification("Error", "An error occurred during check-in", "error");
    });
}

function performCheckOut() {
  showLoading("Checking out...");

  return fetch("/attendance/check-out/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCsrfToken(),
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      hideLoading();
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        showNotification("Check-out Successful", data.message, "success");
        location.reload();
      } else {
        showNotification("Check-out Failed", data.error, "error");
      }
    })
    .catch((error) => {
      hideLoading();
      console.error("Error:", error);
      showNotification("Error", "An error occurred during check-out", "error");
    });
}

// Utility functions
function getCsrfToken() {
  const token = document.querySelector("[name=csrfmiddlewaretoken]");
  return token ? token.value : "";
}

function showLoading(message = "Loading...") {
  const loadingElement = document.createElement("div");
  loadingElement.id = "loading-overlay";
  loadingElement.className =
    "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50";
  loadingElement.innerHTML = `
        <div class="bg-white rounded-lg p-6 flex items-center">
            <div class="spinner"></div>
            <span class="ml-3">${message}</span>
        </div>
    `;

  document.body.appendChild(loadingElement);
}

function hideLoading() {
  const loadingElement = document.getElementById("loading-overlay");
  if (loadingElement) {
    loadingElement.remove();
  }
}

function formatDuration(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${hours}h ${minutes}m`;
}

function formatTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleTimeString("en-US", {
    hour12: true,
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

// Export functions
function exportTableToCSV(tableId, filename) {
  const table = document.getElementById(tableId);
  if (!table) return;

  let csv = [];
  const rows = table.querySelectorAll("tr");

  rows.forEach((row) => {
    const cells = row.querySelectorAll("th, td");
    const rowData = Array.from(cells).map((cell) => {
      return '"' + cell.textContent.trim().replace(/"/g, '""') + '"';
    });
    csv.push(rowData.join(","));
  });

  downloadCSV(csv.join("\n"), filename);
}

function downloadCSV(csvContent, filename) {
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");

  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// Theme functions
function toggleTheme() {
  const body = document.body;
  const isDark = body.classList.contains("dark-mode");

  if (isDark) {
    body.classList.remove("dark-mode");
    localStorage.setItem("theme", "light");
  } else {
    body.classList.add("dark-mode");
    localStorage.setItem("theme", "dark");
  }
}

function initializeTheme() {
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
    document.body.classList.add("dark-mode");
  }
}

// Initialize theme on load
initializeTheme();

// Clean up intervals when page unloads
window.addEventListener("beforeunload", function () {
  if (clockInterval) {
    clearInterval(clockInterval);
  }
});

// Global error handler
window.addEventListener("error", function (e) {
  console.error("Global error:", e.error);
  // You can send error reports to your server here
});

// Service Worker registration (for PWA capabilities)
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/sw.js")
      .then(function (registration) {
        console.log("ServiceWorker registration successful");
      })
      .catch(function (err) {
        console.log("ServiceWorker registration failed");
      });
  });
}
