import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set Matplotlib to use non-interactive backend
import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
import base64
import numpy as np

def upload_csv(request):
    if request.method == 'POST':
        before_file = request.FILES['before_file']
        after_file = request.FILES['after_file']
        
        # Read CSV files
        before_data = pd.read_csv(before_file)
        after_data = pd.read_csv(after_file)
        
        # Perform comparison
        comparison_results = compare_data(before_data, after_data)
        comparison_results_line = compare_data_line(before_data, after_data)
        # Generate graphs
        overall_graph, overall_accuracy, overall_variance = generate_overall_difference_graph(comparison_results)
        
        # Generate individual frequency band plots
        overall_graph_with_line, line_accuracy, line_variance = generate_overall_line_graph(comparison_results_line)
        
        # Generate topographical plots
        topographical_plot_before = generate_topographical_plot(before_data, title="Before")
        topographical_plot_after = generate_topographical_plot(after_data, title="After")
        
        # Calculate overall accuracy and variance
        overall_accuracy_before, overall_variance_before = calculate_overall_accuracy_and_variance(before_data, after_data)
        
        return render(request, 'results.html', {'overall_graph': overall_graph,  
                                                'overall_graph_with_line': overall_graph_with_line,
                                                'topographical_plot_before': topographical_plot_before,
                                                'topographical_plot_after': topographical_plot_after,
                                                'overall_accuracy': overall_accuracy,
                                                'overall_variance': overall_variance,
                                                'line_accuracy': line_accuracy,
                                                'line_variance': line_variance,
                                                'overall_accuracy_before': overall_accuracy_before,
                                                'overall_variance_before': overall_variance_before})
    else:
        return render(request, 'upload.html')


def generate_overall_line_graph(comparison_results):
    fig, axs = plt.subplots(len(comparison_results), 1, figsize=(10, 6 * len(comparison_results)))
    overall_accuracy = {}
    overall_variance = {}
    
    for i, (band, data) in enumerate(comparison_results.items()):
        ax = axs[i] if len(comparison_results) > 1 else axs
        ax.plot(data.index, data['Before'], label='Before', marker='o')
        ax.plot(data.index, data['After'], label='After', marker='o')
        ax.plot(data.index, data['Threshold'], label='Threshold', linestyle=':', color='red')
        ax.legend()
        ax.set_xlabel('Time')
        ax.set_ylabel('Mean Difference')
        ax.set_title(f'Overall Mean Difference for {band} Band Before and After Comparison')
        
        # Calculate accuracy and variance
        accuracy = calculate_accuracy(data['Before'], data['After'], data['Threshold'])
        variance = calculate_variance(data['Before'], data['After'])
        overall_accuracy[band] = accuracy
        overall_variance[band] = variance
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    overall_graph_base64_line = base64.b64encode(buffer.read()).decode('utf-8')
    
    return overall_graph_base64_line, overall_accuracy, overall_variance


def calculate_accuracy(before, after, threshold):
    # Count the number of data points where the absolute difference exceeds the threshold
    exceeding_threshold = np.abs(before - after) > threshold
    total_exceeding = np.sum(exceeding_threshold)
    total_data_points = len(before)
    accuracy = total_exceeding / total_data_points if total_data_points > 0 else 0.0  # Ensure not to divide by zero
    return accuracy


def calculate_variance(before, after):
    diff = np.abs(before - after)
    variance = np.mean(diff)
    return variance


def compare_data_line(before_data, after_data):
    frequency_bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
    comparison_results = {}
    
    for band in frequency_bands:
        band_columns = [col for col in before_data.columns if band in col]
        before_band_mean = before_data[band_columns].mean()
        after_band_mean = after_data[band_columns].mean()
        threshold_value = (before_band_mean + after_band_mean) / 2
        
        comparison_results[band] = pd.DataFrame({
            'Before': before_band_mean,
            'After': after_band_mean,
            'Threshold': threshold_value
        })
    
    return comparison_results


def generate_topographical_plot(data, title):
    # Extract EEG electrode data from the dataframe
    electrode_data = data.drop(columns=['TimeStamp', 'RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10', 'AUX_RIGHT', 'Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'HeadBandOn', 'HSI_TP9', 'HSI_AF7', 'HSI_AF8', 'HSI_TP10', 'Battery', 'Elements'])

    # Assuming electrode data columns are in the form: [Delta_TP9, Delta_AF7, ..., Gamma_TP10]
    # Reshape the data to have 2D representation for topographical plot
    num_channels = 4  # Assuming 4 channels for simplicity
    channel_names = electrode_data.columns
    num_samples = len(electrode_data)
    reshaped_data = electrode_data.values.reshape(num_samples, num_channels, -1)

    # Calculate mean activity across all electrodes
    mean_activity = reshaped_data.mean(axis=1)

    # Create topographical representation as a heat map
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(mean_activity.T, cmap='jet', aspect='auto', interpolation='nearest')
    ax.set_title(f'Topographical Representation ({title})')
    ax.set_xlabel('Time')
    ax.set_ylabel('Electrodes')
    ax.set_yticks(np.arange(len(channel_names)))
    ax.set_yticklabels(channel_names)

    # Add a colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Mean Activity')

    # Convert plot to base64 encoding
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    topographical_plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return topographical_plot_base64


def compare_data(before_data, after_data):
    frequency_bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
    comparison_results = {}
    
    for band in frequency_bands:
        band_columns = [col for col in before_data.columns if band in col]
        before_band_mean = before_data[band_columns].mean(axis=1)
        after_band_mean = after_data[band_columns].mean(axis=1)
        threshold_value = (before_band_mean + after_band_mean) / 2
        
        comparison_results[band] = pd.DataFrame({
            'Before': before_band_mean,
            'After': after_band_mean,
            'Threshold': threshold_value
        })
    
    return comparison_results

def generate_overall_difference_graph(comparison_results):
    fig, axs = plt.subplots(len(comparison_results), 1, figsize=(10, 6 * len(comparison_results)))
    overall_accuracy = {}
    overall_variance = {}
    
    for i, (band, data) in enumerate(comparison_results.items()):
        ax = axs[i] if len(comparison_results) > 1 else axs
        ax.plot(data.index, data['Before'], label='Before', marker='o')
        ax.plot(data.index, data['After'], label='After', marker='o')
        ax.plot(data.index, data['Threshold'], label='Threshold', linestyle=':', color='red')
        ax.legend()
        ax.set_xlabel('Time')
        ax.set_ylabel('Mean Difference')
        ax.set_title(f'Overall Mean Difference for {band} Band Before and After Comparison')
        
        # Calculate accuracy and variance
        accuracy = calculate_accuracy(data['Before'], data['After'], data['Threshold'])
        variance = calculate_variance(data['Before'], data['After'])
        overall_accuracy[band] = accuracy
        overall_variance[band] = variance
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    overall_graph_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    return overall_graph_base64, overall_accuracy, overall_variance

def calculate_overall_accuracy_and_variance(before_data, after_data):
    overall_accuracy = {}
    overall_variance = {}
    
    for band in before_data.columns:
        before_band = pd.to_numeric(before_data[band], errors='coerce')  # Convert to numeric, coercing errors to NaN
        after_band = pd.to_numeric(after_data[band], errors='coerce')    # Convert to numeric, coercing errors to NaN
        
        # Drop NaN values
        before_band = before_band.dropna()
        after_band = after_band.dropna()
        
        print(f"Band: {band}")
        print(f"Before data type: {before_band.dtype}")
        print(f"After data type: {after_band.dtype}")
        
        # Check if there's any data left after dropping NaN values
        if len(before_band) > 0 and len(after_band) > 0:
            accuracy = calculate_accuracy(before_band, after_band, (before_band + after_band) / 2)
            variance = calculate_variance(before_band, after_band)
            overall_accuracy[band] = accuracy
            overall_variance[band] = variance
        else:
            # Handle case where there's no valid data for the band
            overall_accuracy[band] = 0.0
            overall_variance[band] = np.nan
    
    return overall_accuracy, overall_variance



