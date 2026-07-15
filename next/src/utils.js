export const getOrdinal = n => {
  if (n > 3 && n < 21) return "th"; 
  switch (n % 10) {
    case 1:  return "st";
    case 2:  return "nd";
    case 3:  return "rd";
    default: return "th";
  }
}

export const formatDate = (timestamp, compress=false) => {
  /**
   * Converts a timestamp to a date string.
   */

  const date = new Date(timestamp);
  const day = date.getDate();
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const shortMonthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const monthName = compress ? shortMonthNames[date.getMonth()] : monthNames[date.getMonth()];
  return `${day}${compress ? "" : getOrdinal(day)} ${monthName} ${date.getFullYear()}`;
}


export const slugify = text => {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}


export const bookCategoryColor = category => {
  const textColor = {
    1: "text-blue-700",
    2: "text-sky-700",
    3: "text-cyan-700",
    4: "text-orange-700",
    5: "text-red-700",
    6: "text-purple-700",
    7: "text-pink-700",
    undefined: "text-slate-400",
  }[category?.number];
  const blockColor = {
    1: "bg-blue-700",
    2: "bg-sky-700",
    3: "bg-cyan-700",
    4: "bg-orange-700",
    5: "bg-red-700",
    6: "bg-purple-700",
    7: "bg-pink-700",
    undefined: "bg-slate-400",
  }[category?.number];
  return { textColor, blockColor }
}
