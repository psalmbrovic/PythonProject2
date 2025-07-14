import os
import json
from datetime import datetime
from typing import Dict, List, Any


class HTMLReportGenerator:
	"""Generate custom HTML test reports"""

	def __init__(self, report_dir: str = "reports"):
		self.report_dir = report_dir
		os.makedirs(report_dir, exist_ok=True)

	def generate_report(self, test_results: List[Dict[str, Any]], report_name: str = None) -> str:
		"""Generate HTML report from test results"""
		report_name = report_name or f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
		report_path = os.path.join(self.report_dir, report_name)

		# Calculate summary statistics
		total_tests = len(test_results)
		passed_tests = sum(1 for result in test_results if result.get('status') == 'PASSED')
		failed_tests = sum(1 for result in test_results if result.get('status') == 'FAILED')
		skipped_tests = sum(1 for result in test_results if result.get('status') == 'SKIPPED')

		pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

		# Generate HTML content
		html_content = self._generate_html_template(
			test_results, total_tests, passed_tests, failed_tests, skipped_tests, pass_rate
		)

		# Write to file
		with open(report_path, 'w', encoding='utf-8') as file:
			file.write(html_content)

		return report_path

	def _generate_html_template(self, test_results: List[Dict], total: int, passed: int,
	                            failed: int, skipped: int, pass_rate: float) -> str:
		"""Generate HTML template with test results"""

		# Generate test rows
		test_rows = ""
		for i, result in enumerate(test_results, 1):
			status_class = result.get('status', 'UNKNOWN').lower()
			duration = result.get('duration', 0)
			screenshot_link = ""

			if result.get('screenshot'):
				screenshot_link = f'<a href="{result["screenshot"]}" target="_blank">📷 View</a>'

			test_rows += f"""
                <tr class="{status_class}">
                    <td>{i}</td>
                    <td>{result.get('test_name', 'Unknown')}</td>
                    <td>{result.get('test_class', 'Unknown')}</td>
                    <td><span class="status {status_class}">{result.get('status', 'UNKNOWN')}</span></td>
                    <td>{duration:.2f}s</td>
                    <td>{result.get('error_message', '')}</td>
                    <td>{screenshot_link}</td>
                </tr>
            """

		return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Execution Report</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f5f5f5;
                    color: #333;
                    line-height: 1.6;
                }}

                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}

                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    text-align: center;
                }}

                .header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}

                .header .timestamp {{
                    opacity: 0.9;
                    font-size: 1.1em;
                }}

                .summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}

                .summary-card {{
                    background: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                    transition: transform 0.3s ease;
                }}

                .summary-card:hover {{
                    transform: translateY(-5px);
                }}

                .summary-card h3 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    font-weight: bold;
                }}

                .summary-card p {{
                    color: #666;
                    font-size: 1.1em;
                }}

                .total {{ color: #3498db; }}
                .passed {{ color: #27ae60; }}
                .failed {{ color: #e74c3c; }}
                .skipped {{ color: #f39c12; }}

                .pass-rate {{
                    background: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 30px;
                    text-align: center;
                }}

                .progress-bar {{
                    width: 100%;
                    height: 30px;
                    background: #ecf0f1;
                    border-radius: 15px;
                    overflow: hidden;
                    margin: 15px 0;
                }}

                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #27ae60, #2ecc71);
                    width: {pass_rate}%;
                    transition: width 1s ease;
                }}

                .tests-table {{
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}

                .table-header {{
                    background: #34495e;
                    color: white;
                    padding: 20px;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}

                th, td {{
                    padding: 15px;
                    text-align: left;
                    border-bottom: 1px solid #ecf0f1;
                }}

                th {{
                    background: #34495e;
                    color: white;
                    font-weight: 600;
                }}

                tr:hover {{
                    background: #f8f9fa;
                }}

                .status {{
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-weight: bold;
                    text-transform: uppercase;
                    font-size: 0.8em;
                }}

                .status.passed {{
                    background: #d4edda;
                    color: #155724;
                }}

                .status.failed {{
                    background: #f8d7da;
                    color: #721c24;
                }}

                .status.skipped {{
                    background: #fff3cd;
                    color: #856404;
                }}

                .error-message {{
                    max-width: 300px;
                    word-wrap: break-word;
                    font-size: 0.9em;
                    color: #e74c3c;
                }}

                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding: 20px;
                    color: #666;
                }}

                @media (max-width: 768px) {{
                    .container {{
                        padding: 10px;
                    }}

                    .summary {{
                        grid-template-columns: 1fr;
                    }}

                    table {{
                        font-size: 0.9em;
                    }}

                    th, td {{
                        padding: 10px 5px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Test Execution Report</h1>
                    <div class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>

                <div class="summary">
                    <div class="summary-card">
                        <h3 class="total">{total}</h3>
                        <p>Total Tests</p>
                    </div>
                    <div class="summary-card">
                        <h3 class="passed">{passed}</h3>
                        <p>Passed</p>
                    </div>
                    <div class="summary-card">
                        <h3 class="failed">{failed}</h3>
                        <p>Failed</p>
                    </div>
                    <div class="summary-card">
                        <h3 class="skipped">{skipped}</h3>
                        <p>Skipped</p>
                    </div>
                </div>

                <div class="pass-rate">
                    <h2>Pass Rate: {pass_rate:.1f}%</h2>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                </div>

                <div class="tests-table">
                    <div class="table-header">
                        <h2>📋 Test Results Details</h2>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Test Name</th>
                                <th>Test Class</th>
                                <th>Status</th>
                                <th>Duration</th>
                                <th>Error Message</th>
                                <th>Screenshot</th>
                            </tr>
                        </thead>
                        <tbody>
                            {test_rows}
                        </tbody>
                    </table>
                </div>

                <div class="footer">
                    <p>🔧 Generated by Selenium Test Framework | © 2024</p>
                </div>
            </div>

            <script>
                // Add some interactivity
                document.addEventListener('DOMContentLoaded', function() {{
                    // Animate progress bar
                    setTimeout(() => {{
                        const progressBar = document.querySelector('.progress-fill');
                        progressBar.style.width = '{pass_rate}%';
                    }}, 500);

                    // Add click to expand error messages
                    document.querySelectorAll('.error-message').forEach(cell => {{
                        if (cell.textContent.length > 50) {{
                            const fullText = cell.textContent;
                            const shortText = fullText.substring(0, 50) + '...';
                            cell.textContent = shortText;
                            cell.style.cursor = 'pointer';
                            cell.title = 'Click to expand';

                            cell.addEventListener('click', function() {{
                                if (this.textContent === shortText) {{
                                    this.textContent = fullText;
                                    this.title = 'Click to collapse';
                                }} else {{
                                    this.textContent = shortText;
                                    this.title = 'Click to expand';
                                }}
                            }});
                        }}
                    }});
                }});
            </script>
        </body>
        </html>
	"""