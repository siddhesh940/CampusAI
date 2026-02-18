"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { paymentService } from "@/services/campus-services";
import type { Payment } from "@/types";
import {
    CheckCircle2,
    Clock,
    CreditCard,
    Download,
    IndianRupee,
    Loader2,
    Plus,
    XCircle,
} from "lucide-react";
import { useEffect, useState } from "react";

const PAYMENT_TYPES = [
  { value: "tuition_fee", label: "Tuition Fee" },
  { value: "hostel_fee", label: "Hostel Fee" },
  { value: "exam_fee", label: "Exam Fee" },
  { value: "library_fee", label: "Library Fee" },
  { value: "lab_fee", label: "Lab Fee" },
  { value: "registration_fee", label: "Registration Fee" },
  { value: "other", label: "Other" },
];

function StatusBadge({ status }: { status: string }) {
  const cfg: Record<
    string,
    { bg: string; text: string; icon: React.ElementType }
  > = {
    completed: {
      bg: "bg-green-100 dark:bg-green-900/30",
      text: "text-green-700 dark:text-green-400",
      icon: CheckCircle2,
    },
    pending: {
      bg: "bg-yellow-100 dark:bg-yellow-900/30",
      text: "text-yellow-700 dark:text-yellow-400",
      icon: Clock,
    },
    failed: {
      bg: "bg-red-100 dark:bg-red-900/30",
      text: "text-red-700 dark:text-red-400",
      icon: XCircle,
    },
    refunded: {
      bg: "bg-gray-100 dark:bg-gray-800/30",
      text: "text-gray-600 dark:text-gray-400",
      icon: XCircle,
    },
  };
  const c = cfg[status] || cfg.pending;
  const Icon = c.icon;
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${c.bg} ${c.text}`}
    >
      <Icon className="h-3 w-3" />
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}

export default function PaymentsPage() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [verifying, setVerifying] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");

  // Form state
  const [paymentType, setPaymentType] = useState(PAYMENT_TYPES[0].value);
  const [amount, setAmount] = useState("");
  const [notes, setNotes] = useState("");

  const fetchPayments = async () => {
    try {
      const res = await paymentService.list();
      setPayments(res.payments || []);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  const handleInitiate = async () => {
    if (!amount || Number(amount) <= 0) {
      setFormError("Enter a valid amount");
      return;
    }
    setSubmitting(true);
    setFormError("");
    try {
      await paymentService.initiate({
        payment_type: paymentType,
        amount: Number(amount),
        currency: "INR",
        notes: notes || undefined,
      });
      setShowForm(false);
      setAmount("");
      setNotes("");
      await fetchPayments();
    } catch (e: any) {
      setFormError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleVerify = async (paymentId: string) => {
    setVerifying(paymentId);
    try {
      await paymentService.verify(paymentId);
      await fetchPayments();
    } catch {
      // silent
    } finally {
      setVerifying(null);
    }
  };

  const totalPaid = payments
    .filter((p) => p.status === "completed")
    .reduce((s, p) => s + p.amount, 0);
  const totalPending = payments
    .filter((p) => p.status === "pending")
    .reduce((s, p) => s + p.amount, 0);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-40" />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Skeleton className="h-24 rounded-xl" />
          <Skeleton className="h-24 rounded-xl" />
          <Skeleton className="h-24 rounded-xl" />
        </div>
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Payments</h1>
          <p className="text-muted-foreground">
            View and manage your fee payments.
          </p>
        </div>
        <Button variant="gradient" onClick={() => setShowForm(!showForm)}>
          <Plus className="h-4 w-4 mr-2" />
          New Payment
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-card p-4">
          <p className="text-sm text-muted-foreground">Total Paid</p>
          <p className="text-2xl font-bold text-green-600 dark:text-green-400 flex items-center gap-1">
            <IndianRupee className="h-5 w-5" />
            {totalPaid.toLocaleString()}
          </p>
        </div>
        <div className="glass-card p-4">
          <p className="text-sm text-muted-foreground">Pending</p>
          <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-400 flex items-center gap-1">
            <IndianRupee className="h-5 w-5" />
            {totalPending.toLocaleString()}
          </p>
        </div>
        <div className="glass-card p-4">
          <p className="text-sm text-muted-foreground">Total Transactions</p>
          <p className="text-2xl font-bold">{payments.length}</p>
        </div>
      </div>

      {/* New Payment Form */}
      {showForm && (
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold mb-4">Initiate Payment</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <select
              value={paymentType}
              onChange={(e) => setPaymentType(e.target.value)}
              title="Payment type"
              aria-label="Payment type"
              className="flex h-10 rounded-lg border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {PAYMENT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
            <Input
              type="number"
              placeholder="Amount (₹)"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              min="1"
            />
            <Input
              placeholder="Notes (optional)"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
          </div>
          <div className="flex gap-2 mt-4">
            <Button
              onClick={handleInitiate}
              disabled={submitting}
              variant="gradient"
            >
              {submitting ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <CreditCard className="h-4 w-4 mr-2" />
              )}
              {submitting ? "Processing..." : "Pay Now"}
            </Button>
            <Button variant="outline" onClick={() => setShowForm(false)}>
              Cancel
            </Button>
          </div>
          {formError && (
            <p className="text-sm text-red-500 mt-2">{formError}</p>
          )}
        </div>
      )}

      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Payments List */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold mb-4">Transaction History</h2>
        {payments.length === 0 ? (
          <div className="text-center py-12">
            <CreditCard className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
            <p className="text-muted-foreground">No payments yet.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Type
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Amount
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Status
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Transaction ID
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Date
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {payments.map((p) => (
                  <tr
                    key={p.id}
                    className="border-b last:border-0 hover:bg-muted/50 transition-colors"
                  >
                    <td className="py-3 px-2 capitalize">
                      {p.payment_type.replace(/_/g, " ")}
                    </td>
                    <td className="py-3 px-2 font-medium">
                      ₹{p.amount.toLocaleString()}
                    </td>
                    <td className="py-3 px-2">
                      <StatusBadge status={p.status} />
                    </td>
                    <td className="py-3 px-2 text-muted-foreground font-mono text-xs">
                      {p.transaction_id || "—"}
                    </td>
                    <td className="py-3 px-2 text-muted-foreground">
                      {new Date(p.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-2">
                      <div className="flex gap-2">
                        {p.status === "pending" && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleVerify(p.id)}
                            disabled={verifying === p.id}
                          >
                            {verifying === p.id ? (
                              <Loader2 className="h-3 w-3 animate-spin" />
                            ) : (
                              "Verify"
                            )}
                          </Button>
                        )}
                        {p.status === "completed" && (
                          <a
                            href={paymentService.getReceiptUrl(p.id)}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            <Button size="sm" variant="ghost">
                              <Download className="h-3 w-3 mr-1" />
                              Receipt
                            </Button>
                          </a>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
