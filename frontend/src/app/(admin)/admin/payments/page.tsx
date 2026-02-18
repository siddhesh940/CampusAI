"use client";

import { Skeleton } from "@/components/ui/skeleton";
import { adminService } from "@/services/campus-services";
import type { Payment } from "@/types";
import {
    CheckCircle2,
    Clock,
    CreditCard,
    IndianRupee,
    XCircle,
} from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";

const STATUS_TABS = [
  { value: "all", label: "All" },
  { value: "pending", label: "Pending" },
  { value: "completed", label: "Completed" },
  { value: "failed", label: "Failed" },
  { value: "refunded", label: "Refunded" },
];

function StatusBadge({ status }: { status: string }) {
  const cfg: Record<
    string,
    { bg: string; text: string; icon: React.ElementType }
  > = {
    completed: {
      bg: "bg-green-100",
      text: "text-green-700",
      icon: CheckCircle2,
    },
    pending: { bg: "bg-yellow-100", text: "text-yellow-700", icon: Clock },
    failed: { bg: "bg-red-100", text: "text-red-700", icon: XCircle },
    refunded: { bg: "bg-blue-100", text: "text-blue-700", icon: CreditCard },
  };
  const c = cfg[status] || cfg.pending;
  const Icon = c.icon;
  return (
    <span
      className={`inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-full font-medium ${c.bg} ${c.text}`}
    >
      <Icon className="h-3 w-3" />
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}

export default function AdminPaymentsPage() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("all");
  const [total, setTotal] = useState(0);

  const loadPayments = async () => {
    setLoading(true);
    try {
      const res = await adminService.listPayments(activeTab);
      setPayments(res.payments || []);
      setTotal(res.total || 0);
    } catch {
      toast.error("Failed to load payments");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPayments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab]);

  const totalRevenue = payments
    .filter((p) => p.status === ("completed" as any))
    .reduce((sum, p) => sum + p.amount, 0);

  const pendingAmount = payments
    .filter((p) => p.status === ("pending" as any))
    .reduce((sum, p) => sum + p.amount, 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <CreditCard className="h-7 w-7 text-primary" />
          Payment Management
        </h1>
        <p className="text-muted-foreground mt-1">
          View and track all student payments
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <div className="flex items-center gap-2">
            <IndianRupee className="h-4 w-4 text-green-600" />
            <p className="text-sm text-muted-foreground">Total Revenue</p>
          </div>
          <p className="text-2xl font-bold mt-1 text-green-600">
            ₹{totalRevenue.toLocaleString()}
          </p>
        </div>
        <div className="glass-card p-5">
          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4 text-yellow-600" />
            <p className="text-sm text-muted-foreground">Pending</p>
          </div>
          <p className="text-2xl font-bold mt-1 text-yellow-600">
            ₹{pendingAmount.toLocaleString()}
          </p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Total Transactions</p>
          <p className="text-2xl font-bold mt-1">{total}</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-1 bg-muted p-1 rounded-lg w-fit">
        {STATUS_TABS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setActiveTab(tab.value)}
            className={`px-4 py-2 text-sm font-medium rounded-md transition ${
              activeTab === tab.value
                ? "bg-background shadow text-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Table */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-14 w-full" />
          ))}
        </div>
      ) : (
        <div className="glass-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-muted/30">
                  <th className="text-left p-4 font-medium">Transaction ID</th>
                  <th className="text-left p-4 font-medium">Type</th>
                  <th className="text-left p-4 font-medium">Amount</th>
                  <th className="text-left p-4 font-medium">Status</th>
                  <th className="text-left p-4 font-medium">Date</th>
                </tr>
              </thead>
              <tbody>
                {payments.length === 0 ? (
                  <tr>
                    <td
                      colSpan={5}
                      className="p-8 text-center text-muted-foreground"
                    >
                      No payments found.
                    </td>
                  </tr>
                ) : (
                  payments.map((p) => (
                    <tr key={p.id} className="border-b hover:bg-muted/20">
                      <td className="p-4 font-mono text-xs">
                        {p.transaction_id || p.id.slice(0, 8)}
                      </td>
                      <td className="p-4 capitalize">{p.payment_type}</td>
                      <td className="p-4 font-medium">
                        ₹{p.amount.toLocaleString()}
                      </td>
                      <td className="p-4">
                        <StatusBadge status={p.status as string} />
                      </td>
                      <td className="p-4 text-muted-foreground">
                        {new Date(p.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
