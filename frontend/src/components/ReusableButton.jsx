import React from 'react';

const ReusableButton = ({ children, onClick, variant = 'primary', startIcon, fullWidth = false, disabled = false, size = 'medium' }) => {
  const baseClasses = 'border-none rounded-lg font-medium cursor-pointer transition-all duration-200 inline-flex items-center gap-2 text-left';
  const sizeClasses = {
    small: 'px-4 py-2 text-sm',
    medium: 'px-6 py-3 text-base',
    large: 'px-8 py-4 text-lg'
  };
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60',
    outlined: 'bg-transparent text-blue-600 border border-blue-600 hover:bg-blue-50 disabled:opacity-60'
  };
  const widthClasses = fullWidth ? 'w-full justify-center' : '';
  const disabledClasses = disabled ? 'cursor-not-allowed' : '';

  return (
    <button
      className={`${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${widthClasses} ${disabledClasses}`}
      onClick={onClick}
      disabled={disabled}
    >
      {startIcon && <span>{startIcon}</span>}
      {children}
    </button>
  );
};

export default ReusableButton;
