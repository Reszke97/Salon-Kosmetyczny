export const formatDate = (dateToFormat) => {
    if (dateToFormat) {
      if (/(\d{4}-\d{2}-\d{2})/.test(dateToFormat)) {
        return dateToFormat;
      }
      let resultVariable = dateToFormat.toLocaleString("pl", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      });
      const [day, month, year] = resultVariable.split(".");
      return [year, month, day].join("-");
    }
    return "";
  };
  