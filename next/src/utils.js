export const getOrdinal = n => {
  if (n > 3 && n < 21) return "th"; 
  switch (n % 10) {
    case 1:  return "st";
    case 2:  return "nd";
    case 3:  return "rd";
    default: return "th";
  }
}

export const formatDate = timestamp => {
  /**
   * Converts a timestamp to a date string.
   */

  const date = new Date(timestamp);
  const day = date.getDate();
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const monthName = monthNames[date.getMonth()];
  return `${day}${getOrdinal(day)} ${monthName} ${date.getFullYear()}`;
}
